import random
import time
import streamlit as st

st.set_page_config(page_title="가위바위보 말판 게임", layout="wide")

BOARD_SIZE = 10  # 칸 수 (요청: 총 10칸)
PLAYER_EMOJI = "🙂"
COMP_EMOJI = "🤖"


def safe_rerun():
    """Streamlit의 버전 차이로 st.experimental_rerun이 없을 때를 대비한 안전한 호출 래퍼.
    존재하면 호출하고, 없거나 호출 중 에러가 나면 무시한다.
    """
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
    except Exception:
        # 재실행이 지원되지 않거나 내부에서 에러가 나면 무시
        pass

def init_state():
    if "player_pos" not in st.session_state:
        st.session_state.player_pos = 0
    if "comp_pos" not in st.session_state:
        st.session_state.comp_pos = 0
    if "turn" not in st.session_state:
        st.session_state.turn = 0
    if "last_result" not in st.session_state:
        st.session_state.last_result = ""
    if "last_player_choice" not in st.session_state:
        st.session_state.last_player_choice = ""
    if "last_comp_choice" not in st.session_state:
        st.session_state.last_comp_choice = ""
    if "game_over" not in st.session_state:
        st.session_state.game_over = False


def rps_winner(p, c):
    # p, c are '가위','바위','보'
    if p == c:
        return "tie"
    wins = {"가위": "보", "바위": "가위", "보": "바위"}
    if wins[p] == c:
        return "player"
    return "comp"


init_state()

st.title("가위바위보 말판 게임")
st.write("플레이어는 매 턴 가위/바위/보 중 하나를 선택합니다. 이기면 말판이 앞으로 한 칸 이동합니다. 먼저 도착 칸에 도달하면 승리합니다.")

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("턴 정보")
    st.write(f"턴: {st.session_state.turn}")
    st.write(f"플레이어 위치: {st.session_state.player_pos} / {BOARD_SIZE-1}")
    st.write(f"컴퓨터 위치: {st.session_state.comp_pos} / {BOARD_SIZE-1}")
    st.write("---")
    # 결과 및 알림을 표시할 자리
    message_area = st.empty()

    if st.session_state.game_over:
        player_won = st.session_state.player_pos >= BOARD_SIZE - 1
        if player_won:
            st.success("축하합니다! 플레이어가 결승에 도착해 승리했습니다! 🎉")
            try:
                st.balloons()
            except Exception:
                pass
            st.error("컴퓨터는 패배했습니다.")
        else:
            st.error("컴퓨터가 결승에 도착해 승리했습니다.")
            st.info("플레이어는 패배했습니다.")

        if st.button("다시 시작"):
            # 명시적으로 초기값으로 재설정
            st.session_state.player_pos = 0
            st.session_state.comp_pos = 0
            st.session_state.turn = 0
            st.session_state.last_result = ""
            st.session_state.last_player_choice = ""
            st.session_state.last_comp_choice = ""
            st.session_state.game_over = False
            # Streamlit은 버튼 클릭 후 자동으로 스크립트를 다시 실행하더라도
            # 일부 환경/버전에서 명시적 rerun 호출이 있었을 때 AttributeError가 발생할 수 있어
            # 안전한 래퍼를 호출해 재실행을 시도합니다(없으면 무시).
            safe_rerun()
    else:
        # 더 크고 시각적인 선택지: 이모지 + 라벨을 가진 버튼을 사용
        st.subheader("가위/바위/보 선택")
        cols = st.columns(3)
        choices = [("✂️", "가위"), ("✊", "바위"), ("🖐️", "보")]
        clicked = None
        for col, (emoji, label) in zip(cols, choices):
            # 버튼 텍스트에 이모지와 라벨을 같이 표시
            if col.button(f"{emoji}  {label}", key=f"btn_{label}"):
                clicked = label

        if clicked:
            # 컴퓨터 선택
            comp_choice = random.choice(["가위", "바위", "보"])
            st.session_state.last_player_choice = clicked
            st.session_state.last_comp_choice = comp_choice
            result = rps_winner(clicked, comp_choice)
            st.session_state.turn += 1
            if result == "player":
                # 먼저 결과 문구를 준비
                st.session_state.last_result = "플레이어가 이겼습니다! 플레이어가 한 칸 전진합니다."
                # 바로 위치를 갱신하여 이후 보드 렌더링 시 반영되게 함
                st.session_state.player_pos += 1
            elif result == "comp":
                st.session_state.last_result = "컴퓨터가 이겼습니다! 컴퓨터가 한 칸 전진합니다."
                st.session_state.comp_pos += 1
            else:
                st.session_state.last_result = "무승부입니다. 말은 움직이지 않습니다."

            # 승리 체크
            if st.session_state.player_pos >= BOARD_SIZE - 1 or st.session_state.comp_pos >= BOARD_SIZE - 1:
                st.session_state.game_over = True

            # 컴퓨터 선택을 크게 잠시 보여주고, 이어서 결과 문구를 바로 표시
            try:
                message_area.markdown(f"<div style='font-size:22px; font-weight:600;'>컴퓨터는 {comp_choice}를 선택했어요! 🎯</div>", unsafe_allow_html=True)
                time.sleep(0.8)
            except Exception:
                # 시간지연이 환경에 따라 제한될 수 있으므로 실패해도 계속
                pass

            # 결과를 즉시 하이라이트하여 위치 변경 이유를 명확히 보여줌
            message_area.markdown(f"<div style='font-size:18px;'><strong>{st.session_state.last_result}</strong><br><br>플레이어: {st.session_state.last_player_choice}  |  컴퓨터: {st.session_state.last_comp_choice}</div>", unsafe_allow_html=True)

    # Note: detailed last_result block moved into message_area to keep feedback near the board

with col1:
    # 보드 그리기 (상태 업데이트 후 렌더링하여 이동이 즉시 보이도록 함)
    cells = st.columns(BOARD_SIZE)
    for i, c in enumerate(cells):
        content = f"<div style='border:1px solid #ddd; padding:10px; text-align:center; min-width:60px;'>"
        content += f"<div style='font-weight:bold'>{i}</div>"
        tokens = []
        if st.session_state.player_pos == i:
            tokens.append(PLAYER_EMOJI)
        if st.session_state.comp_pos == i:
            tokens.append(COMP_EMOJI)
        if tokens:
            content += "<div style='font-size:24px; margin-top:6px;'>" + " ".join(tokens) + "</div>"
        else:
            content += "<div style='color:#888; margin-top:18px;'>-</div>"
        content += "</div>"
        c.markdown(content, unsafe_allow_html=True)

st.write("\n\n---\nMade with Streamlit")
