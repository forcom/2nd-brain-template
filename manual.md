# LLM Wiki 운영 매뉴얼

핵심부터 말하면, `llm-wiki`는 별도의 앱이나 데이터베이스가 아니라 “에이전트가 이 저장소를 안전하게 편집하는 작업 규칙”입니다. 이 저장소에서는 [SCHEMA.md](SCHEMA.md)가 최우선 계약입니다.

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
1. 원문을 raw/articles/에 출처 URL·수집일·sha256과 함께 캡처
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

현재 Zotero MCP 연결은 동작하고 있습니다. ChromaDB 1.5.9도 Zotero MCP의 격리된 Python
환경에 설치돼 있으며, 의미 검색 DB에는 문서 `1`개가 색인돼 있습니다. Zotero 자료가
변경되면 다음 명령으로 색인을 갱신할 수 있습니다.

```bash
zotero-mcp update-db
zotero-mcp db-status
```

ChromaDB는 Zotero 의미 검색용 색인입니다. `llm-wiki`의 저장소도 아니고, 아래 설명할 지식그래프 저장소도 아닙니다.

## 2. 추가된 소스를 어떻게 편집하는가

폴더마다 규칙이 다릅니다.

| 위치 | 편집 방법 |
|---|---|
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
/Users/y/dev/2nd-brain-template 위키의 지식그래프를 생성해줘.
```

생성 후:

```text
understand-dashboard로
/Users/y/dev/2nd-brain-template 그래프를 열어줘.
```

대시보드는 로컬 URL과 `?token=...`이 포함된 주소를 반환합니다. 이 토큰 URL은 로컬에서만 사용하고 커밋하거나 공유하지 않는 것이 좋습니다.

그래프 저장 경로에는 버전 차이가 있습니다.

- 기존 워크플로 문서는 `.ua/knowledge-graph.json`을 사용합니다.
- 현재 설치된 스킬은 `.understand-anything/knowledge-graph.json`을 생성합니다.
- [.gitignore](.gitignore)는 두 경로를 모두 제외합니다.

현재 checkout에는 `.understand-anything/knowledge-graph.json`과 `meta.json`이 생성되어
있지만 재생성 가능한 로컬 파생 상태이므로 Git에는 포함되지 않습니다. 실행할 때는
[UA 워크플로 문서](queries/ua-knowledge-graph-workflow.md#권장-실행-순서)의 개념을 따르되,
실제 설치된 스킬이 반환하는 경로를 기준으로 대시보드를 여는 것이 안전합니다.

## 4. 이미지 속 Hermes 관련 항목

이미지의 Hermes 부분은 현재 설치 상태가 아니라 [목표 자동화 설계](docs/architecture/second-brain-pkm-architecture.md#7-hermes-자동화-설계)입니다.

| 이미지 항목 | 실제 의미 |
|---|---|
| Hermes Agent | 웹 검색·브라우저·MCP·파일 도구를 실행하는 별도 에이전트 |
| Hermes Cron | 정해진 시간에 새 에이전트 세션을 만들어 작업하는 스케줄러 |
| Hermes Runtime | `~/.hermes/` 아래의 설정, 작업 정의, 세션, 실행 이력, 결과물 전체를 가리키는 운영 상태 |
| `collect-evidence` | 우리가 정의할 수집 작업 이름이지 별도 제품이 아님 |
| `compile-wiki` | `llm-wiki`를 실행하는 작업 이름 |
| `build-knowledge-graph` | UA 그래프를 만드는 작업 이름 |
| `deliver-review` | diff·lint·graph 결과를 사람에게 전달하는 작업 이름이지 Hermes 명령어가 아님 |
| Gate A/B/C | 설치형 도구가 아니라 원본·위키·그래프 검증 체크리스트 |

Hermes의 `web_search`/`web_extract`는 정적 자료 수집에, browser는 동적 사이트 조작에 사용합니다. Zotero는 MCP로 연결할 수 있습니다. [공식 Web Search 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search), [Browser 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser/), [MCP 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)를 참고할 수 있습니다.

현재 이 Mac에는 Hermes가 설치되어 있습니다. 다른 환경에서 처음 도입할 때만 다음 설치를
실행합니다.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup --portal
```

설치 후 Hermes에도 Zotero MCP를 별도로 등록해야 합니다. Codex/Orca 설정은 Hermes가 자동 상속하지 않습니다.

```bash
hermes mcp add zotero \
  --command /Users/y/.local/bin/zotero-mcp \
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

처음에는 그래프까지 무인화하기보다 canonical 컴파일만 리뷰 작업으로 예약하는 것을 권합니다.

```bash
hermes cron create "0 2 * * *" \
  "Read SCHEMA.md, index.md, and recent log.md. Process only validated new raw records on a review branch. Run the full wiki contract checks. Do not merge or push. Return the diff and validation report." \
  --workdir /Users/y/dev/2nd-brain-template \
  --skill llm-wiki \
  --name "compile-wiki"
```

Cron은 매번 새 세션을 만들므로 `--workdir`와 자기완결적인 지시가 중요합니다. 작업 정의와 출력은 `~/.hermes/cron/`에 저장되고, 실행에는 gateway가 필요합니다. [Hermes Cron 공식 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)를 따릅니다.

```bash
hermes gateway install
hermes cron status
```

## 지금 권장하는 실제 순서

1. 웹 URL 한 개로 수동 `llm-wiki` ingest 테스트
2. Obsidian에서 raw와 canonical 변경 검토
3. 검토된 변경을 커밋한 뒤 `understand-knowledge`로 그래프 재생성
4. `understand-dashboard`로 시각 확인
5. Hermes `compile-wiki`를 리뷰 브랜치 작업으로 예약
6. 이후 Gate A→B→C가 확실해지면 그래프 재생성까지 자동화
