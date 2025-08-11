# path: test_diversity_layer.py
from __future__ import annotations

import argparse
import asyncio
import math
import os
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional


try:
    from openai import OpenAI
except Exception as e:
    print("OpenAI SDK가 필요합니다. `pip install openai`", file=sys.stderr)
    raise

# ------------------------ Metrics ------------------------

def pairwise_similarity(texts: List[str]) -> float:
    if len(texts) < 2:
        return 0.0
    sims = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            sims.append(SequenceMatcher(None, texts[i], texts[j]).ratio())
    return float(statistics.mean(sims)) if sims else 0.0

def ngram_diversity(texts: List[str], n: int) -> float:
    grams: Counter[str] = Counter()
    total = 0
    for t in texts:
        s = t.strip()
        seq = [s[i:i+n] for i in range(len(s) - n + 1)]
        grams.update(seq)
        total += max(0, len(s) - n + 1)
    return (len(grams) / total) if total else 0.0

def char_entropy(texts: List[str]) -> float:
    c = Counter("".join(texts))
    tot = sum(c.values())
    if tot == 0:
        return 0.0
    return -sum((v/tot) * math.log2(v/tot) for v in c.values())

def truncate(s: str, width: int = 120) -> str:
    s = s.replace("\n", " ")
    return s if len(s) <= width else s[:width] + "…"

def report(name: str, texts: List[str]) -> None:
    uniq = len(set(texts))
    print(f"\n=== {name} ===")
    print(f"- total: {len(texts)}")
    print(f"- unique: {uniq}")
    print(f"- avg_pairwise_similarity: {pairwise_similarity(texts):.3f}  (낮을수록 다양)")
    print(f"- bigram_diversity: {ngram_diversity(texts, 2):.3f}  (높을수록 다양)")
    print(f"- trigram_diversity: {ngram_diversity(texts, 3):.3f}  (높을수록 다양)")
    print(f"- char_entropy: {char_entropy(texts):.3f}")
    print("- samples:")
    for i, t in enumerate(texts[:5], 1):
        print(f"  {i:02d}. {truncate(t)}")

# ------------------------ Baseline Generator ------------------------

@dataclass(frozen=True)
class Sampling:
    temperature: float = 0.8
    top_p: float = 1.0
    presence_penalty: float = 0.5
    frequency_penalty: float = 0.7
    max_tokens: int = 96

class Baseline:
    def __init__(self, model: str, api_key: Optional[str] = None) -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY 환경변수가 필요합니다.")
        self.client = OpenAI(api_key=key)
        self.model = model

    async def one(self, system: str, user: str, s: Sampling) -> str:
        # 미세 지터로 병렬 도달 타이밍 분산
        await asyncio.sleep(random.uniform(0.01, 0.05))
        resp = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model,
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}],
            temperature=s.temperature,
            top_p=s.top_p,
            presence_penalty=s.presence_penalty,
            frequency_penalty=s.frequency_penalty,
            max_tokens=s.max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()

# ------------------------ Diversity Layer ------------------------

@dataclass
class SamplingSpace:
    t_low: float = 0.75
    t_high: float = 1.10  # was 1.05
    pp_low: float = 0.3
    pp_high: float = 0.8
    fp_low: float = 0.5
    fp_high: float = 0.9
    top_p: float = 1.0
    max_tokens: int = 96

    def sample(self) -> Tuple[float, float, float]:
        return (
            random.uniform(self.t_low, self.t_high),
            random.uniform(self.pp_low, self.pp_high),
            random.uniform(self.fp_low, self.fp_high),
        )

class DiversityLayer:
    """프롬프트 그대로 유지. m개 후보 생성 → MMR로 1개 선택. 키별 메모리로 중복 억제."""
    def __init__(self, model: str, api_key: Optional[str] = None,
                 candidates: int = 5, mmr_alpha: float = 0.6,
                 ngram_n: int = 3, memory_size: int = 128) -> None:
        self.bigram_hist: Dict[str, Counter[str]] = defaultdict(Counter)  # key -> bigram freq
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY 환경변수가 필요합니다.")
        self.client = OpenAI(api_key=key)
        self.model = model
        self.candidates = candidates
        self.alpha = mmr_alpha
        self.ngram_n = ngram_n
        self.memory_size = memory_size
        self.memory: Dict[str, List[str]] = defaultdict(list)
        self.space = SamplingSpace()

    # 3) 보조 함수들 (클래스 안에 추가)
    def _bigrams(self, s: str) -> List[str]:
        s = s.strip()
        return [s[i:i+2] for i in range(max(0, len(s)-1))]

    def _bigram_penalty(self, key: str, text: str) -> float:
        """
        최근 메모리에서 자주 등장한 빅램일수록 페널티↑ (범용, 금지어 하드코딩 없음)
        값 범위 대략 0~1 근처.
        """
        hist = self.bigram_hist.get(key, None)
        if not hist:
            return 0.0
        grams = self._bigrams(text)
        if not grams:
            return 0.0
        # 상위 빈도 빅램일수록 더 감점
        total = 0.0
        for g in grams:
            total += hist.get(g, 0)
        # 정규화: 최근 메모리 크기에 비례해 완만하게
        denom = sum(hist.values()) or 1
        return min(1.0, total / denom)

    def _quality(self, s: str) -> float:
        L = len(s)
        if L < 8: return 0.2
        if L > 120: return 0.4
        q = 0.6 + (0.2 if s.endswith(("。",".","!","?")) else 0.0)
        punct = sum(1 for ch in s if ch in "\"'`[]{}()")
        return max(0.0, min(1.0, q - min(0.3, punct * 0.03)))

    def _counts(self, s: str, n: int) -> Counter[str]:
        s = s.strip()
        return Counter([s[i:i+n] for i in range(max(0, len(s)-n+1))])

    def _overlap(self, a: str, b: str, n: int) -> float:
        ca, cb = self._counts(a, n), self._counts(b, n)
        if not ca or not cb: return 0.0
        inter = sum((ca & cb).values())
        denom = min(sum(ca.values()), sum(cb.values()))
        return inter/denom if denom else 0.0

    def _mem_penalty(self, key: str, text: str) -> float:
        hist = self.memory.get(key, [])[-self.memory_size:]
        if not hist: return 0.0
        ng = [self._overlap(text, h, self.ngram_n) for h in hist]
        sim = [SequenceMatcher(None, text, h).ratio() for h in hist]
        return (sum(ng)/len(ng))*0.6 + (sum(sim)/len(sim))*0.4

    async def _one_candidate(self, system: str, user: str) -> str:
        # 마이크로 지터 + 샘플링 랜덤화
        await asyncio.sleep(random.uniform(0.008, 0.04))
        t, pp, fp = self.space.sample()
        resp = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model,
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}],
            temperature=t, top_p=self.space.top_p,
            presence_penalty=pp, frequency_penalty=fp,
            max_tokens=self.space.max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()

    async def generate(self, key: str, system: str, user: str) -> str:
        cands = await asyncio.gather(*[asyncio.create_task(self._one_candidate(system, user))
                                   for _ in range(self.candidates)])
        best_i, best_score = 0, -1e9
        for i, c in enumerate(cands):
            q = self._quality(c)
            with_others = 0.0
            if len(cands) > 1:
                sims = [SequenceMatcher(None, c, o).ratio() for j, o in enumerate(cands) if j != i]
                with_others = sum(sims) / len(sims)
            bg = self._bigram_penalty(key, c)
            red = 0.55 * self._mem_penalty(key, c) + 0.35 * with_others + 0.10 * bg
            score = self.alpha * q - (1 - self.alpha) * red
            if score > best_score:
                best_score, best_i = score, i
        chosen = cands[best_i]

        # 🔹 최근 결과와 너무 비슷하면 다른 후보로 교체
        def too_similar(a: str, b: str, th: float = 0.90) -> bool:
            return SequenceMatcher(None, a, b).ratio() >= th
        if any(too_similar(chosen, h) for h in self.memory[key][-8:]):
            alt_i, alt_score = best_i, -1e9
            for i, c in enumerate(cands):
                if i == best_i:
                    continue
                q = self._quality(c)
                red = 0.6 * self._mem_penalty(key, c) + 0.4 * SequenceMatcher(None, c, chosen).ratio()
                score = self.alpha * q - (1 - self.alpha) * red
                if score > alt_score:
                    alt_score, alt_i = score, i
            chosen = cands[alt_i]

        mem = self.memory[key]
        mem.append(chosen)
        if len(mem) > self.memory_size:
            del mem[: len(mem) - self.memory_size]

            
        # 빅램 히스토리 업데이트 (최근 텍스트 반영)
        self.bigram_hist[key].update(self._bigrams(chosen))
        # 히스토리가 너무 커지지 않게 상위 N개만 유지 (예: 2000개)
        if sum(self.bigram_hist[key].values()) > 2000:
            self.bigram_hist[key] = Counter(dict(self.bigram_hist[key].most_common(1500)))


        return chosen

# ------------------------ Prompts ------------------------

def build_user_prompt(word: str, base_prompt: Optional[str]) -> str:
    if base_prompt:
        return base_prompt.replace("{word}", word)
    # 기본 프롬프트(범용)
    return (f"日本語で『{word}』を必ず含めた自然な例文を1文だけ生成してください。"
            f"句点で終え、説明/翻訳/引用符 없이 문장만 출력.")

SYSTEM = "Answer exactly as instructed. Output one sentence only."

# ------------------------ Runners ------------------------

async def run_serial(fn, n: int) -> List[str]:
    out: List[str] = []
    for _ in range(n):
        out.append(await fn())
    return out

async def run_parallel(fn, n: int, concurrency: int) -> List[str]:
    sem = asyncio.Semaphore(concurrency)
    async def task():
        async with sem:
            return await fn()
    return await asyncio.gather(*[asyncio.create_task(task()) for _ in range(n)])

# ------------------------ CLI ------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="병렬 다양성 테스트 (Baseline vs Diversity Layer)")
    p.add_argument("--model", default="gpt-4o-mini")
    p.add_argument("--word", default="本質")
    p.add_argument("--prompt", default=None,
                   help="사용자 프롬프트. {word} 자리표시자 지원. 미지정 시 기본 프롬프트 사용")
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--candidates", type=int, default=5)
    p.add_argument("--mmr_alpha", type=float, default=0.6)
    return p.parse_args()

async def amain() -> None:
    args = parse_args()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY 환경변수가 필요합니다.")

    user_prompt = build_user_prompt(args.word, args.prompt)

    base = Baseline(model=args.model, api_key=key)
    s = Sampling()

    div = DiversityLayer(model=args.model, api_key=key,
                         candidates=args.candidates, mmr_alpha=args.mmr_alpha)

    # Baseline
    t0 = time.perf_counter()
    base_serial = await run_serial(lambda: base.one(SYSTEM, user_prompt, s), args.n)
    t1 = time.perf_counter()
    base_parallel = await run_parallel(lambda: base.one(SYSTEM, user_prompt, s), args.n, args.concurrency)
    t2 = time.perf_counter()

    # Diversity Layer
    div_serial = await run_serial(lambda: div.generate(key=args.word, system=SYSTEM, user=user_prompt), args.n)
    t3 = time.perf_counter()
    div_parallel = await run_parallel(lambda: div.generate(key=args.word, system=SYSTEM, user=user_prompt),
                                      args.n, args.concurrency)
    t4 = time.perf_counter()

    print(f"\n[시간] baseline serial: {t1-t0:.2f}s | baseline parallel: {t2-t1:.2f}s | "
          f"div serial: {t3-t2:.2f}s | div parallel: {t4-t3:.2f}s")

    report("BASELINE — SERIAL", base_serial)
    report("BASELINE — PARALLEL", base_parallel)
    report("DIVERSITY — SERIAL", div_serial)
    report("DIVERSITY — PARALLEL", div_parallel)

def main() -> None:
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
