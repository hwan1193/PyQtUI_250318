# PyQtUI_250318
해당 내용은 디자인을 적용하여 소프트웨어의 UI를 통해 유튜브 및 이미지를 볼 수 있는 코드입니다.

## 유튜브 영상 및 이미지 첨부한 내용 UI

![스크린샷 2025-03-18 163229](https://github.com/user-attachments/assets/5ee038cb-3337-4b56-a3d3-67c2610ed878)

## 이 프로젝트는 다음과 같은 기능들을 보여줍니다:

>QEasingCurve를 이용한 사용자 정의 애니메이션:

다양한 애니메이션 효과를 위해, Qt의 QEasingCurve를 사용하여 애니메이션의 움직임을 조절합니다.

>QWebEngineView를 통한 유튜브 영상 삽입:

애플리케이션 내에 웹 브라우저 위젯(QWebEngineView)을 사용하여 유튜브 영상을 직접 재생할 수 있습니다.
동적 UI 속성 (예: Speed)로 애니메이션 제어:
사용자 인터페이스에서 애니메이션의 속도 등을 조절할 수 있는 옵션을 제공합니다.

>필요 조건 (Requirements)

Python 3.7 이상
PySide6
PySide6-WebEngine
(선택 사항) Steamworks Python 바인딩 (Steam 배포 기능을 사용하려면 필요)

>실행 방법 (How to Run)
의존성 설치:
아래 명령어를 터미널이나 명령 프롬프트에 입력하여 필요한 라이브러리를 설치합니다.

>pip install PySide6 PySide6-WebEngine

애플리케이션 실행:
다음 명령어로 애플리케이션을 실행합니다.
>python main.py
