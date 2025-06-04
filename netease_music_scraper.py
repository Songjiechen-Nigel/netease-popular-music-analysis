# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:57:47 2025

@author: Administrator
"""

import requests
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns

# 获取歌曲详情，包括点赞数等
def get_song_detail(song_id):
    url = f"http://music.163.com/api/song/detail/?id={song_id}&ids=[{song_id}]"
    
    # 请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://music.163.com/",
    }
    
    # 发送请求获取响应数据
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # 打印返回的完整数据以检查结构
       # print(json.dumps(data, indent=4, ensure_ascii=False))

        # 确认'songs'字段是否存在
        if 'songs' in data and data['songs']:
            song_info = data['songs'][0]
            
            artists=""
            # 确认 'artists' 字段是否存在
            if 'artists' in song_info and song_info['artists']:
                #for i in (0,len(song_info['artists'])-1):
                for i in range(len(song_info['artists'])):
                    artist = song_info['artists'][i]['name']  # 艺术家名称
                    
                    artists=artists+" "+artist
            else:
                artists = "未知艺术家"
            
            # 获取歌曲名
            name = song_info.get('name', '未知歌曲')
            
            # 获取点赞数/热度（如果字段存在）
            liked_count = song_info.get('popularity', '未知热度')  # 这是歌曲的热度（点赞数可能不同）

            print(f"歌曲: {name} - {artists}")
            print(f"点赞数: {liked_count}")
            
            return {"id": song_id, "name": name, "artists": artists, "popularity": liked_count}
        else:
            print("无法获取歌曲信息")
    else:
        print("获取歌曲详情失败")


# 网易云音乐的歌曲评论接口，需要传入歌曲的ID
def get_song_comments(song_id):
    url = f"http://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit=1"
    
    # 请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://music.163.com/",
    }
    
    # 发送请求获取响应数据
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        
        # 获取评论总数
        comment_count = data['total']
        print(f"评论总数: {comment_count}")
        # 获取热门评论（通常包含点赞数）
        hot_comments = data.get('hotComments', [])
        if hot_comments:
            for comment in hot_comments:
                liked_count = comment['likedCount']
                content = comment['content']
                print(f"热门评论: {content}, 点赞数: {liked_count}")
                
        top_like_count = max([c.get("likedCount", 0) for c in hot_comments], default=0)
        return {"total_comments": comment_count, "top_like_count": top_like_count}
        
    else:
        print("获取评论失败")
        
# 获取网易云飙升榜所有歌曲ID
def get_songs_id(acc):
    # 网易云飙升榜单ID
    playlist_id = '19723756'  # 飙升榜的ID

    url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"

                
    # 请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://music.163.com/",
    }

    # 发送请求获取榜单详情
    
    try:
        response = requests.get(url, headers=headers,timeout=30)
        
        
        if response.status_code == 200:
            data = response.json()
            #print(data)
            #print(data['result'])
            # 获取榜单中的所有歌曲信息
            
            
            if 'result' in data and 'tracks' in data['result']:
                tracks = data['result']['tracks']
                song_ids = []
                
                # 遍历歌曲列表并提取ID
                num=0
                for track in tracks:
                    song_id = track['id']
                    song_name = track['name']
                    artist_name = track['artists'][0]['name']  # 获取第一位歌手名称
                    if num<acc:
                        song_ids.append(song_id)
                        #print(f"歌曲: {song_name} - {artist_name} (ID: {song_id})")
                        num+=1
    
                return song_ids
            else:
                print("暂时无法获取榜单中的歌曲信息")
        else:
            print("获取飙升榜详情失败")
            return []
    except Exception as e:
        print(f"Error fetching top song IDs: {e}")
        return []




def analyze_trends(songs_data):
    """
    Generates visualizations for popularity and comment trends.

    Args:
        songs_data (list): List of dictionaries containing song info and stats.
    """
    names = [song['name'] for song in songs_data]
    popularity = [song['popularity'] for song in songs_data]
    comment_counts = [song['total_comments'] for song in songs_data]
    top_likes = [song['top_like_count'] for song in songs_data]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    sns.barplot(x=popularity, y=names)
    plt.title("Song Popularity")
    plt.xlabel("Popularity")
    plt.ylabel("Song Name")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=comment_counts, y=top_likes, hue=names, palette="tab10")
    plt.title("Comment Count vs Top Comment Likes")
    plt.xlabel("Total Comments")
    plt.ylabel("Top Comment Likes")
    plt.tight_layout()
    plt.show()
    
    
    
    
def main():
    # 输入歌曲ID，调用函数
    song_list=get_songs_id(3)
    #print(song_list)
    songs_data=[]
    for song in song_list:
        song_id =str(song)     #"2674086731"  # 示例歌曲ID（可以替换为你想获取的歌曲ID）
        detail =get_song_detail(song_id)
        print("")
        comments =get_song_comments(song_id)
        print("")
        if detail:
            detail.update(comments)
            songs_data.append(detail)
        time.sleep(1)
        
    analyze_trends(songs_data)


if __name__ == "__main__":
    main()