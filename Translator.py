import sys

dic = [
    ['error','Error Occurred','에러 발생'],
    ['errorlogged','Error is logged in File :\n{}','에러가 다음 파일에 수집되었습니다 :\n{}'],
    ['tab1','𝟏 by 𝟏','𝟏 대 𝟏'],
    ['tab2','𝟏 by 𝒏','𝟏 대 𝒏'],
    ['tab3','𝒏 by 𝒏','𝒏 대 𝒏'],
    ['etc','𝐄𝐭𝐜','기타 설정'],
    ['notsupported','Not Supported','지원되지 않음'],
    ['notsupportedshortcutonthistaberror','Not Supported Shortcut in this Tab.\nUse {} and {} to Interact Each Box.', '이 탭에서는 지원되지 않는 단축키입니다.\n{}과 {}을 이용해 각 객체들과 상호작용하세요.'],
    ['sourcecode','Source Code : {}Repository Link{}','소스 코드 : {}레포지토리 링크{}'],
    ['font','Font : [NanumSquareOTF ac Bold] {}Site Link{}','글꼴 : [나눔스퀘어 ac Bold] {}사이트 링크{}'],
    ['calculateway','Calculate Way Settings','계산 방법 설정'],
    ['bylineorder','By Line Number', '선의 개수로'],
    ['bystrokeorder','By Stroke Order','획의 순서대로'],
    ['invalid','Invalid Input Value','잘못된 입력값'],
    ['invalidmsg','Invalid Input. Please Retry.\nCondition : KR 2 or 3 Letter','잘못된 입력입니다. 다시 시도해주세요.\n조건 : 한글 2자 또는 3자'],
    ['name1','NAME 1','이름 1'],
    ['name2','NAME 2','이름 2'],
    ['analysis','Analysis','조회하기'],
    ['nodata','No Data Exists','데이터가 존재하지 않음'],
    ['nodatamsg','No Data Exists.\nPlease Analysis First.','데이터가 존재하지 않습니다. 먼저 조회해 주세요.'],
    ['duplicateLtoR','Overwrite\nLeft to Right','좌측 항목을\n우측으로 덮기'],
    ['duplicateRtoL','Overwrite\nRight to Left','우측 항목을\n좌측으로 덮기'],
    ['analysistaketime','Analysis (May Not Respond Temporarily)','조회하기 (일시적으로 응답하지 않을 수 있음)'],
    ['adddialog','Add Dialog','항목 입력'],
    ['entertext','Enter text :','텍스트를 입력하세요 :'],
    ['langsetting','Language Setting','언어 설정'],
    ['langsetnotice','You Need to Restart Program to Update Language.','프로그램을 재시작해야 언어가 변경됩니다.'],
    ['information','Information','정보'],
    ['reset','Reset','초기화'],
    ['saveascsv','SAVE AS CSV','CSV 파일로 저장']
]

indexing = []

for d in dic:
    indexing.append(d[0])

def translate(tag, lang):
    try:
        if lang == 'en':
            langaugeNumber = 1
        elif lang == 'ko':
            langaugeNumber = 2
        else:
            langaugeNumber = None
        # print('{} -> {}'.format(tag, dic[indexing.index(tag)][langaugeNumber]))
        return dic[indexing.index(tag)][langaugeNumber]

    except:
        from Checker_GUI import WriteHandledError
        WriteHandledError(external=True)
        sys.exit()