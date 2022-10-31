import os
import requests
import urllib.request
from datetime import datetime

# -------- CONFIG ------------------
# Get your user ID from the "view as visitor link (https://www.midjourney.com/app/users/.../) on your Midjourney gallery
USER_ID = None
# In your browser's dev tools, find the `__Secure-next-auth.session-token` cookie.
SESSION_TOKEN = None
# ---------------------------------

# ------- OPTIONS -----------------
UPSCALES_ONLY = True
GRIDS_ONLY = False
USE_DATE_FOLDERS = True
# ---------------------------------

UA = 'Midjourney-image-downloader/0.0.1'
HEADERS = {'User-Agent': UA}
COOKIES = {'__Secure-next-auth.session-token': SESSION_TOKEN}
ORDER_BY_OPTIONS = ["new", "oldest", "hot", "rising", "top-today", "top-week", "top-month", "top-all", "like_count"]


def get_api_page(order_by="new", page=1):
    api_url = "https://www.midjourney.com/api/app/recent-jobs/" \
              f"?orderBy={order_by}&jobStatus=completed&userId={USER_ID}" \
              f"&dedupe=true&refreshApi=0&amount=50&page={page}"
    if UPSCALES_ONLY:
        api_url += "&jobType=upscale"
    elif GRIDS_ONLY:
        api_url += "&jobType=grid"

    print(f"API URL = {api_url}")
    response = requests.get(api_url, cookies=COOKIES, headers=HEADERS)
    result = response.json()
    return result


def download_page(page):
    for idx, image_json in enumerate(page):
        filename = save_prompt(image_json)
        if filename:
            print(f"{idx+1}/{len(page)} Downloaded {filename}")


def ensure_path_exists(year, month, day, image_id):
    if USE_DATE_FOLDERS:
        if not os.path.isdir(f"jobs/{year}"):
            os.makedirs(f"jobs/{year}")
        if not os.path.isdir(f"jobs/{year}/{month}"):
            os.makedirs(f"jobs/{year}/{month}")
        if not os.path.isdir(f"jobs/{year}/{month}/{day}"):
            os.makedirs(f"jobs/{year}/{month}/{day}")
        if not os.path.isdir(f"jobs/{year}/{month}/{day}/{image_id}"):
            os.makedirs(f"jobs/{year}/{month}/{day}/{image_id}")
        return f"jobs/{year}/{month}/{day}/{image_id}"
    else:
        if not os.path.isdir(f"jobs/{image_id}"):
            os.makedirs(f"jobs/{image_id}")
        return f"jobs/{image_id}"


def save_prompt(image_json):
    image_paths = image_json.get("image_paths", [])
    image_id = image_json.get("id")
    prompt = image_json.get("prompt")
    enqueue_time_str = image_json.get("enqueue_time")
    enqueue_time = datetime.strptime(enqueue_time_str, "%Y-%m-%d %H:%M:%S.%f")
    year = enqueue_time.year
    month = enqueue_time.month
    day = enqueue_time.day

    image_path = ensure_path_exists(year, month, day, image_id)
    filename = prompt.replace(" ", "_").replace(",", "").replace("*", "").replace("'", "").replace(":", "").lower().strip("_*")[:100]
    full_path = f"{image_path}/{filename}.png"

    completed_file_path = f"{image_path}/done"
    image_completed = os.path.isfile(completed_file_path)
    if image_completed:
        print(f"Already downloaded {filename}")
        return
    else:
        for idx, image_url in enumerate(image_paths):
            if idx > 0:
                filename = f"{filename[:97]}-{idx}"
                full_path = f"{image_path}/{filename}.png"
            urllib.request.urlretrieve(image_url, full_path)
        f = open(completed_file_path, "x")
        f.close()
    return full_path


def paginated_download(order_by="new"):
    page = 1
    page_of_results = get_api_page(order_by, page)
    while page_of_results:
        if isinstance(page_of_results, list) and len(page_of_results) > 0 and "no jobs" in page_of_results[0].get("msg", "").lower():
            print("Reached end of available results")
            break

        print(f"Downloading page #{page} (order by '{order_by}')")
        download_page(page_of_results)
        page += 1
        page_of_results = get_api_page(order_by, page)


def download_all_order_by_types():
    for order_by_type in ORDER_BY_OPTIONS:
        paginated_download(order_by_type)


def main():
    if not SESSION_TOKEN or not USER_ID:
        raise Exception("Please edit SESSION_TOKEN and USER_ID")
    download_all_order_by_types()


if __name__ == "__main__":
    main()
