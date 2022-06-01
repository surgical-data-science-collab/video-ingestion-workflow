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

def upload(type, AWS_file_name):

    print("uploading...", AWS_file_name, end=" ")

    if(len(AWS_file_name) < 2): exit()
        
    display_name = os.path.split(AWS_file_name)[1]

    payload = {
        "items": [
            {
                "type": type,
                # The storage key where the file is stored.
                "key": AWS_file_name,
                # This is the display name of the video in the v7 web UI
                "filename": display_name
            }
        ],
        "storage_name": storage_name
    }

    response = requests.put(
        f"https://darwin.v7labs.com/api/teams/{team_slug}/datasets/{dataset_slug}/data",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("request failed", response.text)
    else:
        print("success")

def main():

    n = len(sys.argv)
    print("Total arguments passed:", n)

    if (n<3):
        print("no arguments passed...exiting")
        exit()

    type = sys.argv[1]

    print("uploading type: ", type)
    
    if(type not in ["batch", "image", "video"]):
        print("bad type, try again...exiting")
        exit()

    if(type != "batch"):

        #python3 AWS_darwin_upload.py video video_path
        print("data type: ", type)

        for i in range(2, n):

            print("uploading...", sys.argv[i], end=" ")

            upload(type=type, AWS_file_name=sys.argv[i])

    elif(type == "batch"):

        #python3 AWS_darwin_upload.py batch video file_w_video_paths

        if(len(sys.argv) < 4):
            print("upload type batch but not enough arguments...exiting")
            exit()

        type = sys.argv[2]
        print("data type: ", type)
        print("data file: ", sys.argv[3])

        with open(sys.argv[3], "r", encoding="utf-8") as file:

            for line in file:

                file_name = line.strip()
                upload(type=type, AWS_file_name=file_name)


if __name__ == "__main__":
    main()
