# Proyek Analisis Data : Bike Sharing Dataset

## About Bike Sharing Dataset

[**Bike Sharing Dataset**](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset) is a dataset that contains the hourly and daily count of rental bikes between the years 2011 and 2012 in the [**Capital Bikeshare**](https://capitalbikeshare.com) system with the corresponding weather and seasonal information.

**Dataset Information**

- instant: record index
- dteday : date
- season : season (1:springer, 2:summer, 3:fall, 4:winter)
- yr : year (0: 2011, 1:2012)
- mnth : month ( 1 to 12)
- hr : hour (0 to 23)
- holiday : weather day is holiday or not (extracted from [Web Link])
- weekday : day of the week
- workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
- weathersit :
  - Clear, Few clouds, Partly cloudy, Partly cloudy
  - Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
  - Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
  - Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
- temp : Normalized temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (only in hourly scale)
- atemp: Normalized feeling temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (only in hourly scale)
- hum: Normalized humidity. The values are divided to 100 (max)
- windspeed: Normalized wind speed. The values are divided to 67 (max)
- casual: count of casual users
- registered: count of registered users
- cnt: count of total rental bikes including both casual and registered

## How to Run This Project?

1. Clone this repository

```
git clone https://github.com/Anashaneef/capital-bike-share-analysis.git
```

2. Install all library

```
pip install numpy pandas matplotlib seaborn jupyter streamlit babel
```

or

```
pip install -r requirements.txt
```

3. Go to dashboard folder

```
cd dashboard
```

4. Run with Streamlit

```
streamlit run dashboard.py
```

Or you can or you can directly visit this website

#### [**Click here to view Bike Sharing Dashboard**](https://capital-bike-share-analysis-anashaneef.streamlit.app/)
