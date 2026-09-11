# KB-05 — Source Hunter

공식 원문과 Source-of-Truth 기관을 체계적으로 발굴하고 source registry를 강화한다.

## 목표
링크 수집이 아니라 **누가 원문 권한을 갖는가, 어떤 문서가 canonical한가, 현재 유효한 버전은 무엇인가**를 확인한다.

## 실행
1. 주제별 Source-of-Truth 기관 지도를 만든다.
2. 각 기관에서 법·규정·표준·시장규칙·가이드·시험규정·모델요건·데이터·공청회 자료를 분류한다.
3. 문서별 title, issuer, publication date, effective date, version, status, jurisdiction, source URL, successor document를 확인한다.
4. 동일 문서의 draft/final/revised/superseded 관계를 연결한다.
5. 1차 공식 원문이 없으면 2차 출처를 임시 사용하되 `Reported` 또는 `Unverified`로 표시한다.
6. 자동 감시 가능성을 `Manual / Watch / Automated`로 분류한다.
7. source registry와 evidence gaps를 함께 갱신한다.
8. 핵심 source마다 접근성, 안정적 URL 여부, 변경 감시 방식, 저작권/재배포 조건을 기록한다.

## 출력
- Official Source Map
- Source Priority Matrix
- 신규/갱신 source registry entries
- unresolved source gaps
- watcher 후보 목록

## 금지
검색 결과 요약만 근거로 확정하지 않는다. 중요한 정책·규정·표준의 현재 상태는 가능한 한 공식 원문에서 직접 확인한다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
