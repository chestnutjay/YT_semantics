from apiclient.discovery import build
import json
from csv import writer


vidID = 'lj8TV9q59P4'

def build_service(filename):
    with open(filename) as f:
        key = f.readline()
    print(key)
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=key)


def get_comment(part='snippet',
                maxResults=100,
                textFormat='plainText',
                order='time',
                videoId=vidID,
                csv_filename='christmas_tree_comments'):
    
    # empty lists for storing desired information
    comments, commentsId, repliesCount, likesCount, viewerRating = [],[],[],[],[]

    service = build_service('apikey.json')
    print('finished building service')

    response = service.commentThreads().list(
                                part=part,
                                maxResults=maxResults,
                                textFormat=textFormat,
                                order=order,
                                videoId=videoId,
                                ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['snippet']['topLevelComment']['id']
            reply_count = item['snippet']['totalReplyCount']
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']

            comments.append(comment)
            commentsId.append(comment_id)
            repliesCount.append(reply_count)
            likesCount.append(like_count)

            with open(f'{csv_filename}.csv', 'a+',encoding='utf8') as f:
                csv_writer = writer(f)
                csv_writer.writerow([comment, comment_id, reply_count, like_count])
            print('finished taking 1st batch of comments')

            if 'nextPageToken' in response:
                response = service.commentThreads().list(
                    part=part,
                                maxResults=maxResults,
                                textFormat=textFormat,
                                order=order,
                                videoId=videoId,
                                pageToken=response['nextPageToken']
                                ).execute()
                print('finished 2nd batch comments')
            else:
                break

    print('finished writing comments')
    return {
        'Comments':comments,
        'Comment ID':commentsId,
        'Reply Count':repliesCount,
        'Like Count':likesCount

    }
                            

get_comment()

