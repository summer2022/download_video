import  streamlit as st
from pygments.lexer import default

from dy_videl import *
from video_to_text import *
import os

st.header("将喜欢的视频转成文字吧")
col1, col2 = st.columns(2)
with col1:
    bvid = st.text_input('输入喜欢的视频bvid', '')

with col2:
    local = st.text_input('输入本地文件保存路径', '')
st.divider()


if st.button('获取视频'):
    st.info("程序正在运行...")
    video_path, audio_path = get_bili_video_from_urls(bvid, local)
    if video_path not in st.session_state:
        st.session_state.video_path = video_path
    st.video(st.session_state.video_path)
    st.info(f"完成获取视频，保存在{st.session_state.video_path}")
else:
    try:
        st.video(st.session_state.video_path)
    except:
        st.video("https://www.bilibili.com/video/BV1iJ4m1L7x5/?spm_id_from=333.1387.upload.video_card.click&vd_source=a662fd02be37fa7ced3854d197b52dfb")

st.divider()
if st.button('获取文本'):
    if bvid and local:
        st.info("程序正在运行...")
        audio_path = get_bili_audio_from_urls(bvid, local)
        if audio_path not in st.session_state:
            st.session_state.audio_path = audio_path
        word_path = save_to_word(st.session_state.audio_path, 5,local)
        if word_path not in st.session_state:
            st.session_state.word_path = word_path
        st.info(f"完成获取文本，文本保存在{st.session_state.word_path}")
    else:
        st.info("请输入bvid和本地路径")

else:
    try:
        st.info(f"完成获取文本，文本保存在{st.session_state.word_path}")
    except:
        st.info("尚未点击获取文本")





