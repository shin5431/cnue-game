import random
import streamlit as st

st.set_page_config(page_title="가위바위보 말판 게임", layout="wide")

BOARD_SIZE = 10  # 칸 수 (요청: 총 10칸)
PLAYER_EMOJI = "🙂"
COMP_EMOJI = "🤖"

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

st.title("부루마블 스타일 가위바위보 말판 게임")
st.write("플레이어는 매 턴 가위/바위/보 중 하나를 선택합니다. 이기면 말판이 앞으로 한 칸 이동합니다. 먼저 도착 칸에 도달하면 승리합니다.")

col1, col2 = st.columns([3, 1])

with col1:
    # 보드 그리기
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

with col2:
    st.subheader("턴 정보")
    st.write(f"턴: {st.session_state.turn}")
    st.write(f"플레이어 위치: {st.session_state.player_pos} / {BOARD_SIZE-1}")
    st.write(f"컴퓨터 위치: {st.session_state.comp_pos} / {BOARD_SIZE-1}")
    st.write("---")

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
            for k in ["player_pos", "comp_pos", "turn", "last_result", "last_player_choice", "last_comp_choice", "game_over"]:
                st.session_state[k] = 0 if k in ("player_pos", "comp_pos", "turn") else "" if k != "game_over" else False
            st.experimental_rerun()
    else:
        choice = st.radio("가위/바위/보를 선택하세요:", ("가위", "바위", "보"))
        if st.button("제출"):
            # 컴퓨터 선택
            comp_choice = random.choice(["가위", "바위", "보"])
            st.session_state.last_player_choice = choice
            st.session_state.last_comp_choice = comp_choice
            result = rps_winner(choice, comp_choice)
            st.session_state.turn += 1
            if result == "player":
                st.session_state.player_pos += 1
                st.session_state.last_result = "플레이어가 이겼습니다! 플레이어가 한 칸 전진합니다."
            elif result == "comp":
                st.session_state.comp_pos += 1
                st.session_state.last_result = "컴퓨터가 이겼습니다! 컴퓨터가 한 칸 전진합니다."
            else:
                st.session_state.last_result = "무승부입니다. 말은 움직이지 않습니다."

            # 승리 체크
            if st.session_state.player_pos >= BOARD_SIZE - 1 or st.session_state.comp_pos >= BOARD_SIZE - 1:
                st.session_state.game_over = True

            st.experimental_rerun()

    if st.session_state.last_result:
        st.write("---")
        st.write(f"마지막 결과: {st.session_state.last_result}")
        if st.session_state.last_player_choice:
            st.write(f"플레이어: {st.session_state.last_player_choice}  |  컴퓨터: {st.session_state.last_comp_choice}")

st.write("\n\n---\nMade with Streamlit")
