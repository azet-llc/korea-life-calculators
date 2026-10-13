#!/usr/bin/env python3
"""README 생성: 각 계산기 사이트의 공개 llms.txt(우리가 올린 검증 문구)에서 설명과 계산식 FAQ를 그대로 옮긴다. 숫자를 새로 쓰지 않는다."""
import re, subprocess
SITES = ["yeonbong.fyi","toejikgeum.fyi","silup.fyi","sigeup.fyi","loancalc.fyi","pyeong.fyi","agecalc.fyi","ddaycalc.date","charcount.fyi","makeqr.fyi","pwcheck.fyi"]
SKIP = re.compile(r"방은|방이|방을|크루|친구|공유|저장되|개인정보|서버|광고|무료인가|공식인가|정확한가요")   # 기능 소개·면책 문답은 빼고 계산 기준만
out = ["# 한국 생활 계산기 공식 모음 (Korea life calculators — formulas)", "",
"연봉 실수령액·퇴직금·실업급여·주휴수당·대출 상환·평수·만 나이처럼 자주 찾는 계산의 **기준과 계산식**을 한곳에 모았습니다. 각 항목은 무료 계산기(가입 없음, 브라우저에서 계산)에 실제로 들어 있는 기준 그대로입니다.", "",
"- 틀린 곳이나 바뀐 기준을 보시면 [Issues](../../issues)에, 계산 질문은 [Discussions](../../discussions)에 남겨 주세요. 운영팀이 직접 답합니다.",
"- 여기 적힌 값은 참고용 어림값입니다. 실제 금액은 회사 급여 자료·관할 기관 결정이 기준입니다.", ""]
for d in SITES:
    t = subprocess.run(["curl","-s","-m","20",f"https://{d}/llms.txt"],capture_output=True,text=True).stdout
    ko = re.search(r"\n\n([^\n>#-][^\n]*[가-힣][^\n]*)\n", t)
    title = re.search(r"\(([^)]*[가-힣][^)]*)\)", t.splitlines()[0]) or re.search(r"# (.*)", t)
    sec = t.split("## 자주 묻는 질문 (한국어)")[-1].split("\n## ")[0] if "## 자주 묻는 질문 (한국어)" in t else ""
    faqs = [l for l in sec.splitlines() if l.startswith("- **") and not SKIP.search(l)][:4]
    out += [f"## {title.group(1)} — [{d}](https://{d}/)", "", ko.group(1) if ko else "", ""] + faqs + [""]
    print(d, title.group(1), len(faqs))
out += ["---", "문의는 각 계산기의 문의 페이지로 · 각 계산기의 전체 기준은 사이트의 `/llms-full.txt`에 있습니다. 이 문서의 글은 CC BY 4.0 — 인용할 때 출처(해당 계산기 주소)를 적어 주세요."]
open("README.md","w").write("\n".join(out))
