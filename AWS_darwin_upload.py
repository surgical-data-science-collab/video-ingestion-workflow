import requests
import sys

api_key = "PUT API KEY HERE"

team_slug = "PUT DARWIN TEAM NAME HERE"
dataset_slug = "PUT DATASET NAME HERE"
storage_name = "PUT AWS BUCKET NAME"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"ApiKey {api_key}"
}

def upload(data_type, AWS_file_name, fps="native"):

    print("uploading...", AWS_file_name, end=" ")

    if(len(AWS_file_name) < 2): exit()

    display_name = os.path.split(AWS_file_name)[1]

    payload = {
        "items": [
            {
                "type": data_type,

                "fps": fps,

                # The storage key where the file is stored.
                "key": AWS_file_name,

                # This is the display name of the video in the v7 web UI
                "filename": display_name,

                "as_frames": False,

            }
        ],
        "storage_name": storage_name
    }

    print("\n", payload)

    response = requests.put(
        f"https://darwin.v7labs.com/api/teams/{team_slug}/datasets/{dataset_slug}/data",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("request failed", response.text)
    else:
        print("success", response.text)

def main():

    n = len(sys.argv)
    print("Total arguments passed:", n)

    if (n<3):
        print("no arguments passed...exiting")
        exit()

    data_type = sys.argv[1]
    fps = "native"

    print("uploading data_type: ", data_type)

    if(data_type not in ["batch", "image", "video"]):
        print("bad data_type, try again...exiting")
        exit()

    if(data_type != "batch"):

        #python3 AWS_darwin_upload.py video video_path
        print("data data_type: ", data_type)

        if(data_type == "video"): 
            fps = input("Enter the frame-rate desired (a number or 'native'): ")

            if((fps.isnumeric() == False) and (fps != "native")):
                print("bad fps...exiting")
                exit()

        for i in range(2, n):

            print("uploading...", sys.argv[i], end=" ")

            upload(data_type=data_type, AWS_file_name=sys.argv[i], fps=fps)

    elif(data_type == "batch"):

        #python3 AWS_darwin_upload.py batch video file_w_video_paths

        if(len(sys.argv) < 4):
            print("upload data_type batch but not enough arguments...exiting")
            exit()

        data_type = sys.argv[2]
        print("data type: ", data_type)

        if(data_type == "video"): 
            fps = input("Enter the frame-rate desired (a number or 'native'): ")

            if((fps.isnumeric() == False) and (fps != "native")):
                print("bad fps...exiting")
                exit()

        print("data file: ", sys.argv[3])

        with open(sys.argv[3], "r", encoding="utf-8") as file:

            for line in file:

                file_name = line.strip()
                upload(data_type=data_type, AWS_file_name=file_name, fps=fps)


if __name__ == "__main__":
    main()



'''
Modify the script with your API Key and other information

Download the uploader script AWS_darwin_upload.py
Modify the lines 4-8 with your team's API key, team "slug", dataset "slug", and AWS bucket name (slug names have spaces replaced by a HYPHEN)
Save the script if you have not already
Run the script
NOTE: If the path name has spaces, the script might not work properly. In that case, edits to the script may need to be made.

To upload a single (or a few) image: python3 AWS_darwin_upload.py image {path(s) to image within AWS Bucket}

Example: if "test1.png" and "test2.png" are within a folder called "images" which is within the AWS bucket named "my_bucket":
python3 AWS_darwin_upload.py image images/test1.png images/test2.png

To upload a single (or a few) video:
python3 AWS_darwin_upload.py video {path(s) to video within AWS Bucket}

To upload a batch of images or videos:
python3 AWS_darwin_upload.py batch image {path to text file with AWS Bucket image paths} or
python3 AWS_darwin_upload.py batch video {path to text file with AWS Bucket video paths}

If uploading a batch of videos, the script will prompt you for the frame rate for the upload. Type in either a number (like 5) or the word "native", which means the original frame rate of the video,
NOTE 1: Put quotation marks around the pathname for the file with all the paths NOTE 2: The script will use the name of the video/image file for the display name in Darwin V7 (excluding the rest of the path).

Videos take a long time to fully upload to Darwin, so be patient. Images usually appear in a few minutes but videos may take hours. If there are any issues with the script, you may need to adjust based on your use case.
'''
