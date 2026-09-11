"""Required public/development repository boundary for generated projects."""
from pathlib import Path


def development_root(public_root: Path) -> Path:
    return public_root.with_name(public_root.name + "-dev")


SOURCE_POLICY = """# 원문 보관 및 공개 정책

모든 프로젝트는 공개 저장소 `<name>`과 비공개 개발 저장소 `<name>-dev` 두 개를 반드시 운영합니다.
개발 저장소 이름은 공개 저장소의 전체 이름 뒤에 정확히 `-dev`를 붙입니다.

- 원문은 Source ID, 공식 URL, 발행기관, 버전, 발행일·시행일, 확인일, 페이지·절로 추적합니다.
- 수집한 PDF·HTML·데이터 등 원문 파일과 추출 전문은 비공개 개발 저장소의 `sources/`에 저장하고 Git으로 버전 관리합니다.
- 개발 저장소의 `data/source-archive.yaml`에 Source ID, 공식 URL, 보관 경로, 수집 시각, SHA-256, 버전을 기록합니다. 변경된 원문은 새 버전으로 보관합니다.
- 공개 저장소와 공개 사이트에는 검증된 지식·요약 및 출처 메타데이터를 게시하며, 원문 제공은 발행기관의 공식 URL 링크로만 합니다.
- 원문 파일, 전문 복제, 원문 embed/다운로드, 개발 저장소 경로·URL은 공개 사이트·검색 인덱스·배포 산출물에 포함하지 않습니다.
- 개발 저장소의 원문과 연구 기록은 검토 후 필요한 지식만 공개 저장소로 옮깁니다. 개발 저장소 전체를 복사하거나 Git 이력을 공개 저장소에 병합하지 않습니다.
- 공개 사이트는 공개 저장소만 빌드합니다. Cloud Storage는 비공개 보조 사본이며 개발 저장소 원문 보관을 대체하지 않습니다.
- 원문을 확보하지 못한 경우 개발 저장소에 사유와 후속 작업을 기록합니다. URL만 기록한 상태를 원문 보관 완료로 표시하지 않습니다.
"""

PUBLIC_ATTACHMENTS = """# Attachments

공개 가능한 자체 제작 이미지·도표를 관리합니다.
원문은 공개 저장소에 첨부하지 않고 공식 URL과 Source ID로만 연결합니다.
원문 파일·추출 전문은 비공개 `<공개 저장소명>-dev/sources/`에 저장합니다.
원문 embed나 개발 저장소 보관 경로를 공개 사이트에 노출하지 않습니다.
"""

ARCHIVE_REGISTRY = """version: 1
archives: []

# 비공개 개발 저장소 전용. 공개 Source Registry의 id와 연결합니다.
# - source_id: SRC-0001
#   url: https://example.org/document
#   version: '1.0'
#   archive_path: sources/SRC-0001/2026-09-12/document.pdf
#   retrieved_at: '2026-09-12T00:00:00Z'
#   sha256: '<SHA-256 of the archived file>'
#   status: archived
"""

PUBLIC_IGNORE = """# Original documents and development records belong in the sibling -dev repository.
/sources/
/project/
/gcp/
/data/source-archive.yaml
/data/source-candidates.json
*-dev/
.env
.env.*
__pycache__/
"""
