import pprint
from typing import final

import pandas as pd
import requests
from openpyxl.styles.builtins import title
from sympy.physics.vector.printing import params
from pprint import pprint
import json
from moviepy.editor import VideoFileClip, AudioFileClip
import os



def get_dy_video_from_urls(aweme_id):
    url_list, item_title = get_dy_video_url_list(aweme_id)
    for url in url_list:
        try:
            response = requests.get(url, stream=True)
            # 检查网址是否有效
            if response.status_code == 200:
                print(f'找到有效网址: {url}')
                # 获取视频内容
                video_content = response.content
                # 可以选择保存到文件或进行其他处理
                with open(f'{item_title}.mp4', 'wb') as f:
                    f.write(video_content)
                print('视频已保存')
                break
            else:
                print(f'网址无效: {url}')
        except requests.exceptions.RequestException as e:
            print(f'请求错误: {e}')


def get_dy_video_url_list(aweme_id):
    aweme_id = aweme_id
    url = f"https://douyin.wtf/api/douyin/web/fetch_one_video?aweme_id={aweme_id}"
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    # }
    #
    # params = {
    #     "aweme_id ":aweme_id
    # }
    res = requests.get(url)
    data = res.json()
    # pprint(data)
    item_title = data["data"]["aweme_detail"]["item_title"]
    # pprint(data)
    data = data["data"]["aweme_detail"]["video"]["bit_rate"]
    pprint(item_title)
    mid_data = (data[len(data) //2])
    url_list = mid_data["play_addr"]["url_list"]
    print(url_list)
    return url_list, item_title

def bili_auvidel_url_list(bvid):
    bvid = bvid
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }
    bvid_url = f"https://douyin.wtf/api/bilibili/web/fetch_one_video?bv_id={bvid}"

    res = requests.get(bvid_url,headers= headers)
    data = res.json()
    # pprint(data)
    title = data["data"]["data"]["title"]
    cid = data["data"]["data"]["pages"][0]["cid"]
    pprint(cid)
    data_url = f"https://douyin.wtf/api/bilibili/web/fetch_video_playurl?bv_id={bvid}&cid={cid}"
    res = requests.get(data_url)
    data = res.json()
    audio_url = data["data"]["data"]["dash"]["audio"][1]
    keys = ['backupUrl', 'backup_url', 'baseUrl', 'base_url']
    audio_url_list = [audio_url[key] for key in keys if key in audio_url]
    audio_url_list_f = [item[0] if isinstance(item, list) else item for item in audio_url_list]
    # pprint(audio_url_list_f)
    video_url = data["data"]["data"]["dash"]["video"][0]
    video_url_list = [video_url[key] for key in keys if key in video_url]
    video_url_list_f = [item[0] if isinstance(item, list) else item for item in video_url_list]
    # pprint(video_url_list_f)
    return video_url_list_f,audio_url_list_f





def get_bili_video_from_urls(bvid,path):
    vi_url, au_url = bili_auvidel_url_list(bvid)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }
    # 获取视频文件
    video_path = None
    for url in vi_url:
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            if response.status_code == 200:
                print(f'找到有效视频网址: {url}')
                video_path = os.path.join(path, f'temp_video_{bvid}.mp4')
                # print(video_path)
                with open(video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print('视频已保存')
                break
            else:
                print(f'视频网址无效: {url}')
        except requests.exceptions.RequestException as e:
            print(f'视频请求错误: {e}')

    # 获取音频文件
    audio_path = None
    for url in au_url:
        try:
            response = requests.get(url, headers= headers,stream=True)
            if response.status_code == 200:
                print(f'找到有效音频网址: {url}')
                audio_content = response.content
                audio_path = os.path.join(path,f'temp_audio_{bvid}.mp3')
                with open(audio_path, 'wb') as f:
                    f.write(audio_content)
                print('音频已保存')
                break
            else:
                print(f'音频网址无效: {url}')
        except requests.exceptions.RequestException as e:
            print(f'音频请求错误: {e}')

    # 如果成功获取了视频和音频，则合并它们
    if video_path and audio_path:
        try:
            # 加载视频和音频
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # 将音频添加到视频中
            final_clip = video_clip.set_audio(audio_clip)

            # 输出最终的视频文件
            output_path = os.path.join(path,f'final_video_{bvid}.mp4')
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

            # 关闭剪辑以释放资源
            video_clip.close()
            audio_clip.close()
            final_clip.close()

            print(f'最终视频已保存到: {output_path}')

            # 删除临时文件
            os.remove(video_path)
            # os.remove(audio_path)
        except Exception as e:
            print(f'合并视频和音频时出错: {e}')
    else:
        print('未能获取有效的视频和音频文件')
        output_path = None
    return output_path,audio_path



def get_bili_audio_from_urls(bvid,path):
    vi_url, au_url = bili_auvidel_url_list(bvid)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }

    # 获取音频文件
    audio_path = None
    for url in au_url:
        try:
            response = requests.get(url, headers= headers,stream=True)
            if response.status_code == 200:
                print(f'找到有效音频网址: {url}')
                audio_content = response.content
                audio_path = os.path.join(path,f'temp_audio_{bvid}.mp3')
                with open(audio_path, 'wb') as f:
                    f.write(audio_content)
                print('音频已保存')
                break
            else:
                print(f'音频网址无效: {url}')
        except requests.exceptions.RequestException as e:
            print(f'音频请求错误: {e}')

    return audio_path

if __name__ == '__main__':
    # bvid = "BV1QwEtz8EYg"
    # au_url,vi_url = bili_auvidel_url_list(bvid)
    # print(au_url)
    # print(vi_url)
    audio_path  = get_bili_audio_from_urls("BV1zREQzGETK",r"C:\Users\Administrator\Desktop\B站视频")
