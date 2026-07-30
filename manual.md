# LLM Wiki 운영 매뉴얼

핵심부터 말하면, `llm-wiki`는 별도의 앱이나 데이터베이스가 아니라 “에이전트가 이 저장소를 안전하게 편집하는 작업 규칙”입니다. 이 저장소에서는 [SCHEMA.md](SCHEMA.md)가 최우선 계약입니다.

명령은 저장소 루트에서 실행합니다. 아래 예시의 `WIKI`는 현재 checkout의 절대 경로를
뜻하며, 저장소 안의 문서와 작업 보고에는 사용자별 절대 경로 대신 저장소 상대 경로를
사용합니다.

```bash
WIKI="$(pwd -P)"
test -f "$WIKI/SCHEMA.md" &&
  test -f "$WIKI/index.md" &&
  test -f "$WIKI/log.md"
```

```text
URL·PDF·Zotero·메모
→ inbox/ 임시 보관
→ raw/ 원본 캡처·해시 고정
→ canonical 지식으로 컴파일
→ index.md·log.md·링크 검증
→ Git 검토·커밋
→ 지식그래프 재생성
```

## 1. 소스 추가 방법

### 웹 문서

URL을 바로 에이전트에게 주고 다음처럼 요청하면 됩니다.

```text
llm-wiki로 이 URL을 ingest해줘: <URL>

SCHEMA.md, index.md, 최근 log.md를 먼저 확인하고:
1. 원문 종류에 맞는 SCHEMA 등록 raw 디렉터리에 출처 URL·수집일·sha256과 함께 캡처
2. 기존 canonical 주제와 중복되는지 검색
3. 기존 페이지 갱신 또는 새 페이지 생성 조건 판단
4. sources·wikilink·index.md·log.md까지 동기화
5. 전체 계약을 검증하고 변경 내용을 보고
```

Obsidian Web Clipper를 쓴다면 우선 `inbox/`로 저장하는 편이 안전합니다. Clipper 결과가 바로 `raw/`에 들어가려면 frontmatter와 SHA-256 규칙까지 만족해야 하기 때문입니다.

원본 하나가 추가됐다고 항상 새 canonical 페이지가 만들어지는 것은 아닙니다. 중심 주제이거나 여러 소스에서 반복되는 주제만 승격하고, 이미 있는 주제라면 해당 문서에 근거를 보강합니다. 자세한 흐름은 [README.ko.md](README.ko.md#기본-사용-흐름)에 정리돼 있습니다.

### Zotero 논문

먼저 Zotero Connector로 논문을 Zotero에 추가하고, 가능한 한 제목·저자·DOI·PDF가 있는 부모 항목을 사용합니다. 그다음 정확한 item key, DOI 또는 제목을 지정합니다.

```text
Zotero 부모 항목 <ITEM_KEY 또는 DOI>를 llm-wiki로 ingest해줘.
Zotero MCP로 부모 메타데이터와 full text를 조회하고,
첨부파일 key를 논문 key로 오인하지 마.
raw 원본과 canonical 변경안을 만들고 계약을 검증해줘.
```

현재 [SCHEMA.md](SCHEMA.md#directory-roles)는 `raw/papers/*.md`를 정식 원본 레코드로
등록하고 로컬 PDF 추출·해시 규칙과 Zotero 메타데이터 복구 예외를 정의합니다. 따라서
별도의 디렉터리 등록 없이 논문을 수집할 수 있지만, Zotero 부모 항목의 서지정보와
추출 본문을 함께 보존해야 합니다.

ChromaDB는 Zotero MCP의 선택적 의미 검색 색인입니다. 설치 버전, 문서 수와 갱신 시점은
계속 바뀌므로 매뉴얼에 고정하지 않고 다음 명령으로 현재 상태를 확인합니다. Zotero
자료가 변경되면 색인을 갱신한 뒤 상태를 다시 확인합니다.

```bash
zotero-mcp update-db
zotero-mcp db-status
```

ChromaDB는 Zotero 의미 검색용 색인입니다. `llm-wiki`의 저장소도 아니고, 아래 설명할 지식그래프 저장소도 아닙니다.

## 2. 추가된 소스를 어떻게 편집하는가

폴더마다 규칙이 다릅니다.

| 위치 | 편집 방법 |
| --- | --- |
| `inbox/` | 자유롭게 정리·수정 가능 |
| `raw/` | 최초 캡처 후 본문 수정 금지 |
| `entities/`, `concepts/`, `comparisons/`, `queries/` | 사람이 Obsidian에서 편집하거나 에이전트에게 갱신 요청 가능 |
| `index.md` | canonical 변경과 동시에 갱신 |
| `log.md` | 이전 기록은 건드리지 않고 새 항목만 추가 |

원본에 오류가 있어도 `raw/`를 고치지 않고 canonical 페이지에서 정정과 해석을 기록합니다. 웹 원문이 새 버전으로 변경됐다면 기존 raw를 덮어쓰지 말고 새 캡처를 추가합니다.

Zotero는 스키마가 정의한 “메타데이터 복구”만 예외입니다. 이때도 추출 본문 바이트는 보존하고 해시를 다시 계산해야 합니다. 규칙은 [SCHEMA.md의 Raw source integrity](SCHEMA.md#raw-source-integrity)에 있습니다.

Canonical 문서를 직접 편집했다면 반드시 함께 처리해야 합니다.

- `created` 유지, `updated` 변경
- 실제 존재하는 `raw/*.md`를 `sources`에 추가
- 필요한 주장에 `^[raw/...md]` 표식
- 다른 canonical 페이지로 유효한 `[[wikilink]]` 두 개 이상
- `index.md` 동기화
- `log.md`에 새 작업 기록

따라서 수동 편집 후에는 이렇게 요청하면 좋습니다.

```text
내가 수정한 canonical 문서를 llm-wiki 계약에 맞게 검증해줘.
source, frontmatter, wikilink, index.md, log.md와 raw sha256까지 확인하고
필요한 수정만 적용해줘.
```

## 3. 지식그래프 보는 방법

두 종류가 있습니다.

### Obsidian 기본 그래프

저장소를 Obsidian vault로 연 뒤 Command Palette에서 `Open graph view`를 실행하면 됩니다. 이것은 canonical 문서의 명시적인 `[[wikilink]]`를 즉시 보여줍니다.

그래프 필터에는 다음과 같이 canonical 폴더만 포함시키면 보기 편합니다.

```text
path:entities OR path:concepts OR path:comparisons OR path:queries
```

`.obsidian/`은 Git에서 제외되어 있으므로 개인 그래프 설정은 커밋되지 않습니다.

### Understand Anything 지식그래프

이쪽은 단순 링크뿐 아니라 엔티티·주장·암시적 관계·주제 군집까지 분석한 파생 그래프입니다. 에이전트에게 다음처럼 요청하면 됩니다.

```text
understand-knowledge로
현재 저장소 루트의 위키 지식그래프를 생성해줘.
```

생성 후:

```text
understand-dashboard로
현재 저장소 루트의 그래프를 열어줘.
```

대시보드는 로컬 URL과 `?token=...`이 포함된 주소를 반환합니다. 이 토큰 URL은 로컬에서만 사용하고 커밋하거나 공유하지 않는 것이 좋습니다.

그래프 저장 경로에는 도구 버전 차이가 있습니다.

- 현재 자동화와 검증기는 `.understand-anything/knowledge-graph.json` 및 `meta.json`을
  기준으로 사용합니다.
- 일부 기존 문서·도식의 `.ua/knowledge-graph.json`은 이전 도구가 사용하던 경로입니다.
- [.gitignore](.gitignore)는 이전 `.ua/`, analyzer batch와 intermediate를 제외하고
  `.understand-anything/`의 graph/meta 두 파일만 허용합니다.

현재 checkout에는 `.understand-anything/knowledge-graph.json`과 `meta.json`이 생성되어
있고, 권한 있는 clone이 같은 확장 그래프를 즉시 볼 수 있도록 Git으로 공유합니다.
두 파일은 버전 관리하더라도 재생성 가능한 파생 상태이며 evidence나 canonical은
아닙니다. 실행할 때는
[UA 워크플로 문서](queries/ua-knowledge-graph-workflow.md#권장-실행-순서)의 개념을 따르되,
실제 설치된 스킬이 반환하는 경로를 기준으로 대시보드를 여는 것이 안전합니다.

## 4. Hermes 자동화와 현재 운영 상태

이미지의 Hermes 부분은 [전체 자동화 설계](docs/architecture/second-brain-pkm-architecture.md#7-hermes-자동화-설계)를
표현합니다. 현재는 canonical 컴파일과 그래프 재생성 작업이 예약되어 있고, 자동 수집과
별도 전달 작업은 아직 설계상 작업 이름으로 남아 있습니다.

| 이미지 항목 | 실제 의미 | 현재 상태 |
| --- | --- | --- |
| Hermes Agent | 웹 검색·브라우저·MCP·파일 도구를 실행하는 에이전트 런타임 | 설치됨 |
| Hermes Cron | 정해진 시간에 새 에이전트 세션을 만드는 스케줄러 | 활성 |
| Hermes Runtime | 설정, 작업 정의, 세션, 실행 이력과 전달 결과를 담는 로컬 운영 상태 | `~/.hermes/`에 유지, Git 제외 |
| `collect-evidence` | 허용된 소스를 수집하도록 정의할 수 있는 작업 이름 | 미예약 |
| `compile-wiki` | `llm-wiki`로 변경안을 만드는 리뷰 작업 | 매일 02:00 예약 |
| `build-knowledge-graph` | 이미지의 개념적 작업 이름 | 실제 이름은 `refresh-knowledge-graph`, 매일 03:00 예약 |
| `deliver-review` | diff·검증·그래프 결과를 전달하는 개념적 작업 이름 | 별도 job 미예약, 현재 각 job이 로컬 보고 |
| Gate A/B/C | 저장소의 결정론적 원본·canonical·그래프 검증 단계 | 검사기와 그래프 job에 구현 |

Hermes의 `web_search`/`web_extract`는 정적 자료 수집에, browser는 동적 사이트 조작에 사용합니다. Zotero는 MCP로 연결할 수 있습니다. [공식 Web Search 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search), [Browser 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser/), [MCP 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)를 참고할 수 있습니다.

### 4.1 Hermes와 스킬 설정

이 작성 환경에는 Hermes가 설치되어 있습니다. 다른 환경에서 처음 도입할 때만 설치
명령을 실행합니다.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup --portal
```

Hermes는 Codex/Orca의 MCP 설정을 자동 상속하지 않으므로 Zotero MCP를 별도로
등록합니다. 실행 파일 경로를 고정하기 전에 `command -v` 결과를 확인합니다.

```bash
ZOTERO_MCP_BIN="$(command -v zotero-mcp)"
test -n "$ZOTERO_MCP_BIN"
hermes mcp add zotero \
  --command "$ZOTERO_MCP_BIN" \
  --args serve
```

공유용 `llm-wiki` 원본은
[`.agents/skills/llm-wiki`](.agents/skills/llm-wiki/SKILL.md)에 포함되어 있습니다.
프로젝트 스킬을 지원하는 에이전트는 clone 후 바로 사용할 수 있고, 다른 환경에서는
해당 디렉터리를 그 에이전트의 공식 절차로 등록하거나 복사합니다.

Hermes에는 내장 `llm-wiki`도 활성화되어 있으므로 같은 이름의 커뮤니티 스킬을
`--force`로 중복 설치하지 않습니다.

```bash
hermes skills list
hermes skills diff llm-wiki
```

저장소 공유본과 이 Mac의 Hermes 내장본에는 프로젝트 루트를 현재 작업 디렉터리로
고정하고 Zotero 부모 항목의 서지정보를 먼저 보존하도록 보강했습니다.
`hermes skills diff llm-wiki`는 로컬 내장본의 보강 때문에 변경 사항을 표시하는 것이
정상입니다. 커뮤니티판 보안 검사에서 탐지된 `obsidian-headless`, systemd 상주 서비스,
`sudo loginctl` 절차는 macOS 로컬 vault에 필요하지 않아 공유본에도 포함하지 않았습니다.
Hermes의 기본 스킬 위치와 외부 디렉터리 설정은
[공식 Skills 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)에
설명돼 있습니다.

Understand Anything 스킬은 `llm-wiki`와 이름이 겹치지 않는 해당 플러그인의 `skills`
디렉터리만 외부 경로로 등록합니다. 프로젝트 전체 `.agents/skills`를 등록하면 Hermes
내장 `llm-wiki`와 프로젝트 스킬 이름이 충돌할 수 있으므로 사용하지 않습니다.

```bash
UA_SKILLS_DIR="$HOME/.understand-anything/repo/understand-anything-plugin/skills"
test -d "$UA_SKILLS_DIR"
hermes config set skills.external_dirs "$UA_SKILLS_DIR"
```

### 4.2 예약 작업

현재 운영 순서는 다음과 같습니다.

| 시각 | 작업 | 쓰기 범위 | 다음 단계로 넘기는 조건 |
| --- | --- | --- | --- |
| 매일 02:00 | `compile-wiki` | review 브랜치의 canonical·`index.md`·`log.md` 변경안 | 사람이 검토하고 `main`에 반영 |
| 매일 03:00 | `refresh-knowledge-graph` | versioned graph/meta 두 파일의 review diff | Gate A/B 통과, fingerprint 기록, Gate C 통과 |

`compile-wiki`는 검토안을 만들 뿐 자동 병합하거나 push하지 않습니다. 아직 review
브랜치에만 있는 변경은 03:00 그래프 작업의 입력이 아닙니다. 사람이 승인한 변경이 clean
`main`에 들어간 뒤에만 그래프에 반영됩니다. 두 작업의 시간 간격은 의존성 보장이
아니므로, 그래프 작업은 실행할 때마다 branch·worktree와 Gate를 다시 확인합니다.

기존 작업은 중복 생성하지 말고 먼저 상태와 실행 이력을 확인합니다.

```bash
hermes cron list
hermes cron runs
hermes cron status
```

새 환경에 `compile-wiki`가 없을 때만 다음 예시로 생성합니다.

```bash
hermes cron create "0 2 * * *" \
  "Read SCHEMA.md, index.md, and recent log.md. Process only validated new raw records on a review branch. Run the full wiki contract checks. Do not merge or push. Return the diff and validation report." \
  --workdir "$WIKI" \
  --skill llm-wiki \
  --name "compile-wiki"
```

Cron은 매번 새 세션을 만들므로 `--workdir`와 자기완결적인 지시가 중요합니다. 작업
정의와 출력은 `~/.hermes/cron/`에 저장되고 실행에는 gateway가 필요합니다.
[Hermes Cron 공식 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)를
따릅니다.

```bash
hermes gateway install
hermes cron status
```

### 4.3 Gate 공통 판정 규칙

Gate는 설치형 제품이 아니라 저장소에 포함된
[`validate-wiki.py`](.agents/skills/llm-wiki/scripts/validate-wiki.py)가 판정하는 세
단계 계약입니다. `--gate`를 반복하면 지정한 Gate만 순서대로 검사하고, 생략하면
A·B·C를 모두 검사합니다.

| Gate | 입력 경계 | 성공 결과 | 실패 격리 |
| --- | --- | --- | --- |
| A — Evidence | `raw/**/*.md`, `SCHEMA.md`, `index.md`, `log.md` | 검증된 immutable evidence revision | canonical·graph를 건드리지 않고 중단 |
| B — Canonical | 네 canonical 디렉터리와 schema·index·log | 그래프 입력으로 사용할 수 있는 canonical revision | 기존 graph를 유지하고 중단 |
| C — Graph | versioned graph/meta와 결정론적 입력 fingerprint | 현재 wiki 입력에 대응하는 완전한 파생 graph | 새 graph를 승인하지 않고 이전 상태 복원 |

```bash
# 수동 편집 후 원본과 canonical만 검사
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --gate a --gate b

# 예약 그래프 작업의 사전 검사
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --gate a --gate b --require-clean-main

# 그래프 생성 후 입력 fingerprint 기록
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --write-graph-input-metadata

# graph/meta 두 파일의 변경만 허용해 생성·정리 후 검사
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --gate c --require-clean-main --allow-graph-output-changes

# 이미 commit된 snapshot의 세 Gate를 한 번에 검사
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --require-clean-main
```

공통 판정은 다음과 같습니다.

- 오류가 하나도 없으면 해당 Gate의 `ok`가 `true`이고 프로세스가 성공 코드 `0`을
  반환합니다. 오류가 하나라도 있으면 `ok`가 `false`이고 실패 코드 `1`을 반환합니다.
- `warnings`는 실패가 아닙니다. 현재 허용되는 경고는 `log.md`에 근거가 남은 신뢰된
  legacy raw의 해시·형식 coverage gap입니다. 새 raw에 같은 예외를 적용하면 안 됩니다.
- `--require-clean-main`은 현재 브랜치가 정확히 `main`이고 `git status --porcelain`이
  비어 있을 때만 통과합니다. Git에서 무시되지 않은 미추적 파일도 dirty로 간주합니다.
- 생성 후 검사의 `--allow-graph-output-changes`는 clean 조건을 완화하되 graph/meta
  두 파일만 예외로 인정합니다. 다른 tracked·staged·untracked 변경이 하나라도 있으면
  실패합니다.
- 출력은 `errors`, `warnings`, `metrics`를 포함한 JSON입니다. 지표의 개수 자체를
  고정값으로 비교하지 말고 오류 유무와 현재 저장소의 실제 개수를 함께 봅니다.
- 판정 순서는 A → B → C입니다. 뒤 Gate의 성공이 앞 Gate 실패를 상쇄하지 않습니다.

#### Gate A — Evidence

Gate A는 `raw/` 원본 바이트와 위키 기반 파일이 안전한지를 판정합니다.

| 검사 대상 | 통과 기준 |
| --- | --- |
| 기반 파일 | `SCHEMA.md`, `index.md`, `log.md`가 존재하고 읽을 수 있음 |
| 기반 파일 형식 | UTF-8, BOM 없음, CR 없음, LF 줄바꿈, 마지막 LF 존재 |
| raw 탐색 범위 | `raw/` 아래의 모든 `*.md`를 재귀적으로 검사 |
| raw 파일 형식 | UTF-8, BOM 없음, CR 없음 |
| frontmatter | byte 0의 `---`로 시작하는 경우 닫는 `---`가 있고, 중복 key나 지원하지 않는 중첩 구조가 없는 flat YAML이어야 함 |
| 기록된 `sha256` | 닫는 frontmatter 다음 바이트부터 EOF까지 정확히 SHA-256을 다시 계산한 값과 일치 |
| 해시가 있는 raw | 마지막 LF가 반드시 존재 |
| legacy 예외 | frontmatter 또는 `sha256`이 없으면 경고로 분류하되, 검사기는 해당 저장소 상대 경로가 기존 `log.md`에 기록되어 있는지 확인 |
| 보고 지표 | raw 전체 수, 실제로 재계산한 해시 수, legacy coverage gap 수 |

Gate A가 실패하면 canonical과 그래프를 변경하지 않고 즉시 중단합니다. Gate A의
legacy 경고 허용은 기존 바이트 동일 복사본을 보존하기 위한 좁은 예외입니다. 새로
수집하는 raw는 [SCHEMA.md의 Raw source integrity](SCHEMA.md#raw-source-integrity)에
따라 필수 메타데이터와 `sha256`을 갖춰야 합니다. 검사기는 raw의 모든 도메인별
메타데이터 의미까지 판단하지 않으므로 URL·수집일·문서 식별자·추출 방식이 실제
원문과 맞는지, legacy 복사 기록에 원본·대상 hash와 신뢰 근거가 있는지는 ingest
검토에서 별도로 확인합니다. importer 경로와 raw 본문은 보존하며, Zotero metadata
repair와 NotebookLM mapping 외의 raw 수정은 허용하지 않습니다.

#### Gate B — Canonical

Gate B는 canonical 페이지와 `SCHEMA.md`·`index.md`·`log.md`의 정합성을 판정합니다.

| 검사 대상 | 통과 기준 |
| --- | --- |
| 기반 파일 | `SCHEMA.md`, `index.md`, `log.md`가 UTF-8·LF·BOM 없음·마지막 LF 조건을 만족 |
| canonical 범위 | `entities/`, `concepts/`, `comparisons/`, `queries/` 바로 아래의 `*.md` |
| 파일명과 크기 | lowercase kebab-case `.md`, 마지막 LF 존재, 최대 200줄 |
| frontmatter | byte 0에서 시작하고 닫는 delimiter가 있으며 중복 key·지원하지 않는 중첩이 없는 flat YAML; 필수 9개 필드 `title`, `created`, `updated`, `type`, `tags`, `sources`, `confidence`, `contested`, `contradictions` 존재 |
| 제목·날짜·타입 | 제목은 비어 있지 않은 문자열, 날짜는 ISO 달력 날짜, `updated >= created`, `type`은 디렉터리와 일치 |
| 신뢰도 | `high`, `medium`, `low` 중 하나이며 `high`는 서로 다른 source가 최소 2개 |
| 태그 | list이고 중복이 없으며 모든 값이 `SCHEMA.md` Registered tags에 등록됨 |
| 출처 | list이고 중복 없음; 각 항목은 상대 경로의 기존 raw Markdown이며 `SCHEMA.md`에 등록된 source 디렉터리 아래에 있음 |
| 출처 제외 대상 | 절대 경로, `..`, 비 Markdown, 존재하지 않는 파일, `raw/papers/files/` attachment는 source가 될 수 없음 |
| claim marker | 본문의 모든 `^[raw/...md]`가 실제 파일로 해석되고 같은 페이지의 `sources`에 먼저 등록됨 |
| contestation | `contested`는 boolean, `contradictions`는 list이며 각 slug는 존재하는 다른 active canonical 페이지 |
| wikilink | self-link와 broken canonical link가 없고 페이지마다 서로 다른 non-self canonical target이 최소 2개 |
| slug | 네 canonical 디렉터리 전체에서 중복 없음 |
| `index.md` | 모든 active canonical slug가 정확히 한 번 존재하고 다른 항목은 없음; `Total pages`가 실제 수와 같고 type section이 맞으며 section 안에서 알파벳순 |
| `log.md` | `## [YYYY-MM-DD] action \| subject` 형식이며 날짜가 유효하고 action이 `ingest`, `create`, `update`, `query`, `lint`, `archive`, `delete`, `map`, `repair` 중 하나 |
| 보고 지표 | canonical·index 항목·등록 태그·source 참조·claim marker·유효 link target 수 |

Gate B가 실패하면 그래프 생성이나 교체를 시작하지 않습니다. 다음 항목은 현재 파일 한
벌만 보는 결정론적 검사로는 변경 의도를 완전히 알 수 없으므로 diff와 사람 검토로
추가 확인합니다.

- raw 본문이 과거 revision과 비교해 변경되지 않았는지
- canonical 수정 시 `created`를 보존하고 `updated`를 실제로 올렸는지
- 새 페이지가 중심 주제 또는 두 source 이상에서 반복되는 주제인지, 기존 synonym이
  아닌지
- template에서 남은 `<angle-bracket>` placeholder가 없고, multi-source·contested
  합성처럼 필요한 주장에 claim marker가 실제로 붙었는지
- `contested: true` 본문에 날짜와 출처가 있는 미해결 입장이 실제로 적혀 있는지
- `index.md`의 한 줄 설명이 내용과 맞고 `log.md`가 append-only이며 이번 변경 경로를
  빠짐없이 기록했는지

#### Gate C — Graph

Gate C는 `.understand-anything/knowledge-graph.json`과 `meta.json`이 현재 Git revision의
완전한 파생 그래프인지를 판정합니다.

| 검사 대상 | 통과 기준 |
| --- | --- |
| 파일과 JSON | graph와 meta 두 파일이 존재하고 UTF-8 JSON으로 파싱됨 |
| 그래프 종류 | 최상위 `kind`가 정확히 `knowledge` |
| 컬렉션 | `nodes`와 `edges`가 list이고 `layers`와 `tour`가 비어 있지 않은 list |
| node 필드 | 모든 node가 object이며 `id`, `type`, `name`, `summary`, `tags`, `complexity` key를 가짐 |
| node 식별자 | `id`가 비어 있지 않은 문자열이고 전체에서 유일하며 `tags`는 list |
| article coverage | UA 규칙상 article인 모든 Git-visible Markdown과 graph의 article node 집합이 정확히 일치 |
| source coverage | `raw/` 아래의 모든 non-hidden Git-visible 파일과 graph의 source node 집합이 정확히 일치 |
| canonical coverage | 모든 active canonical 파일에 대응하는 `article:<directory>/<slug>` node가 존재 |
| edge | 모든 edge가 object이고 `source`와 `target`이 문자열 node ID이며 dangling endpoint가 0개 |
| 입력 freshness | `meta.inputHashAlgorithm`이 `sha256-path-size-bytes-v1`이고 현재 입력 hash·파일 수가 `inputHash`·`inputFiles`와 일치 |
| Git provenance | graph와 meta의 `gitCommitHash`가 같은 유효한 generation base commit이며 현재 HEAD와 같거나 그 ancestor |
| 분석 개수 | `meta.analyzedFiles`가 실제 `type: article` node 수와 일치 |
| 분석 시각 | `meta.lastAnalyzedAt`이 ISO-8601로 해석되며 `Z` UTC 표기도 허용 |
| 정리 완료 | `.understand-anything/intermediate/`가 남아 있지 않음 |
| 보고 지표 | node·article/source node·edge·dangling edge·layer·tour step·입력 수와 hash·generation base·HEAD·분석 시각 |

Gate C의 freshness는 graph/meta 자체를 제외하고 UA article, `index.md`, `log.md`와
versioned raw 파일의 상대 경로·크기·정확한 바이트로 계산합니다. graph를 commit하면
HEAD가 바뀌기 때문에 HEAD 동일성은 freshness 기준으로 사용할 수 없습니다.
`gitCommitHash`는 생성 기반 revision의 provenance로 보존하고 content fingerprint를
현재성 판단에 사용합니다. 입력 문서가 하나라도 바뀌면 기존 graph가 stale이 됩니다.
Gate C가 실패해도 raw나 canonical을 수정해서 맞추지 않습니다.

### 4.4 그래프 재생성 트랜잭션

`refresh-knowledge-graph`는 다음 순서를 하나의 실패 격리 트랜잭션으로 수행합니다.

1. branch가 `main`이고 worktree가 clean인지 확인합니다.
2. Gate A와 Gate B를 실행합니다. 하나라도 실패하면 기존 그래프를 그대로 두고
   중단합니다.
3. 기존 그래프에 Gate C를 실행합니다. 현재 입력 fingerprint에서 이미 통과하면 `unchanged`로
   종료하고 재생성하지 않습니다.
4. Gate C 실패 원인이 graph/meta 누락 또는 input fingerprint stale뿐일 때 기존
   graph/meta의 존재 여부와 바이트를 임시 위치에 snapshot합니다. 다른 구조 오류라면
   자동으로 덮어쓰지 않고 실패를 보고합니다.
5. `understand-knowledge`의 모든 article analyzer batch를 완료하고 각 batch JSON을
   파싱 검증한 뒤 병합합니다. 일부 batch 성공만으로 최종 그래프를 만들지 않습니다.
6. 임시 batch 파일과 `.understand-anything/intermediate/`를 개별 대상 기준으로
   정리합니다. 대시보드는 생성 작업에서 열지 않습니다.
7. `--write-graph-input-metadata`로 현재 입력 fingerprint를 기록합니다.
8. 정리 완료 후 graph/meta 두 파일의 변경만 허용한 clean `main` 조건과 Gate C를 다시
   검사합니다.
9. batch·병합·저장·정리·fingerprint·최종 Gate C 중 하나라도 실패하면 snapshot한 이전 graph/meta를
   복원합니다. 이전 파일이 없었다면 부분 생성 파일을 제거하고 실패를 보고합니다.

이 작업은 versioned `knowledge-graph.json`과 `meta.json`만 수정하고, `log.md`나 다른
tracked 파일, Git commit, merge, push를 수행하지 않습니다. 성공하면 두 파일의 review
diff를 남기므로 사람이 검증해 commit해야 다음 실행 전 clean `main`이 복원됩니다.
intermediate와 cache는 계속 [.gitignore](.gitignore)에 의해 제외되며 graph는 canonical
근거로 자동 승격되지 않습니다.

새 환경에 그래프 작업이 없을 때만 다음 정의를 생성합니다.

```bash
hermes cron create "0 3 * * *" \
  "Operate only on clean main. Run python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --gate a --gate b --require-clean-main. If Gate A or B fails, stop and preserve the last valid graph. Run Gate C; if it passes, report an unchanged skip. If it fails only because graph/meta is missing or the input fingerprint is stale, snapshot the old graph/meta bytes and use understand-knowledge to regenerate them. Require every article-analyzer batch to complete and validate each final analysis-batch-N.json with jq. Do not open the dashboard. Clean temporary and intermediate files with individually targeted operations and verify intermediate is absent. Run python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --write-graph-input-metadata, then run Gate C with --require-clean-main --allow-graph-output-changes. Only knowledge-graph.json and meta.json may differ. If any batch, merge, save, cleanup, fingerprint, or final Gate C fails, restore the previous graph/meta or remove partial files when none existed. Report the two-file review diff on success. Do not edit log.md or any other tracked file. Do not commit, merge, or push." \
  --workdir "$WIKI" \
  --skill llm-wiki \
  --skill understand-knowledge \
  --name "refresh-knowledge-graph"
```

## 5. 실제 운영 순서

1. 새 source를 `inbox/`에 두거나 `llm-wiki`로 올바른 `raw/` 레코드로 ingest합니다.
2. Gate A를 통과한 원본만 canonical 변경 후보로 사용합니다.
3. canonical·`index.md`·`log.md`를 하나의 변경으로 검토하고 Gate B를 통과시킵니다.
4. 변경을 commit하고 승인된 revision을 clean `main`에 둡니다.
5. `refresh-knowledge-graph`가 기존 Gate C를 확인해 current이면 건너뛰고 stale이면
   재생성·정리·fingerprint 기록·최종 Gate C를 수행하도록 둡니다.
6. 성공한 graph/meta review diff를 확인해 함께 commit하고 다시 clean `main`으로
   만듭니다.
7. 필요할 때만 `understand-dashboard`로 시각 확인하고, 그래프가 제안한 관계는 raw
   근거를 확인한 뒤 별도의 canonical transaction으로 반영합니다.
8. `hermes cron list`와 `hermes cron runs`로 작업 상태를 확인하고, 실패 시 JSON의 첫
   실패 Gate부터 수정합니다.
