# Stack Phones

## Add New Phones

### 1. Scrape New Phones

On your local machine:

* Update `START` and `END` values in `t.py`
* Run:

```bash
python t.py
```
* Backup New Files

Copy newly added files from: `scraped_pages/` to <https://github.com/suhailvs/stackschools_datas>

---

### 2. Parse Data and Download Images

* Update `TOTAL_PHONES` in `views.py`
* Ensure `scraped_pages/` folder exist in the project root:
* Make sure previously downloaded images are present inside `scraped_pages/images/`

Then:

1. Open the website(https://stackphones.com or http://localhost:8000), at the bottom of the page:
2. Click **parse scraped pages**
   * For a fresh database, this may take around 9 minutes
3. Click **image download**
4. Copy newly added images from `scraped_pages/images/` to <https://github.com/suhailvs/stackschools_datas> and `media` folder.

## Local Setup

```bash
cp .env.sample .env
./manage.py migrate
```


## Similar WEB

+ Global Rank: 817 
+ Total visits: 50M 

Country | Percentage
--- | ---
India | 16.25%
Indonesia | 9.11%
United States | 6.2%
Bangladesh | 3.97%
Pakistan | 3.86%
Others | 60.6%

+ phonearena.com
+ 91mobiles.com
+ nanoreview.net
+ smartprix.com
+ kimovil.com
+ devicespecifications.com
+ gadgets360.com