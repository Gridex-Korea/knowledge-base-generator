# Operational Commands

Knowledge Base Generator는 생성 이후의 운영 작업도 같은 `kbgen` CLI에서 수행합니다.

## Command map

```text
kbgen init       → 새 Knowledge Base 생성
kbgen research   → 연구계획 / grounded source discovery
kbgen audit      → Evidence·metadata 품질 감사
kbgen doctor     → Vault 구조와 validator 상태 점검
kbgen github     → GitHub repository bootstrap 계획/실행
```

기존 `kbgen "해상풍력"` 호출도 `init`의 하위 호환으로 유지합니다.

## 1. Init

```bash
kbgen init "해상풍력" --countries KR AU --site quartz --gcp-level 2
```

또는 기존 방식:

```bash
kbgen "해상풍력" --countries KR AU --site quartz --gcp-level 2
```

## 2. Research plan

네트워크/API 호출 없이 Source-of-Truth 카테고리와 조사 쿼리, 완료조건을 생성합니다.

```bash
kbgen research ./offshore-wind-knowledge-base
```

결과:

```text
project/research-plan.md
```

## 3. Grounded source discovery with Vertex AI

```bash
kbgen research ./offshore-wind-knowledge-base \
  --provider vertex \
  --gcp-project MY_PROJECT \
  --location us-central1 \
  --model gemini-2.5-flash
```

인증은 다음 중 하나를 사용합니다.

```bash
gcloud auth application-default login
# kbgen은 실제 요청 토큰을 gcloud auth print-access-token으로 가져옵니다.
```

또는:

```bash
export GOOGLE_OAUTH_ACCESS_TOKEN=...
```

출력:

```text
project/research-plan.md
project/research-results.md
data/source-candidates.json
```

Google Search grounding이 돌려준 URL은 **Candidate Source**로만 저장됩니다. 공식기관·원문·버전·시행상태를 검증하기 전에는 `Confirmed`로 승격하지 않습니다.

## 4. Evidence audit

```bash
kbgen audit ./offshore-wind-knowledge-base
```

다음을 검사합니다.

- Evidence Level 분포
- `Unverified` note
- source ID가 없는 일반 knowledge note
- `last_verified`가 없는 note
- frontmatter 누락

결과는 기본적으로 `project/evidence-audit.md`에 저장합니다.

## 5. Doctor

```bash
kbgen doctor ./offshore-wind-knowledge-base
```

필수 Vault 구조를 확인하고 생성된 `scripts/validate_kb.py`까지 실제 실행합니다.

## 6. GitHub bootstrap

기본은 dry-run입니다.

```bash
kbgen github ./offshore-wind-knowledge-base --owner Uptec-khj
```

실제 저장소 생성·초기 push:

```bash
kbgen github ./offshore-wind-knowledge-base \
  --owner Uptec-khj \
  --execute
```

이 명령은 로컬의 `git`과 GitHub CLI `gh`를 사용합니다. `--execute` 없이는 원격 변경을 수행하지 않습니다.

## Recommended lifecycle

```text
kbgen init
   ↓
kbgen research
   ↓
Candidate Sources
   ↓
원문 검증 / Source Registry 승격
   ↓
Knowledge Note 작성
   ↓
kbgen audit
   ↓
kbgen doctor
   ↓
GitHub PR / merge
   ↓
정기 research + audit
```
