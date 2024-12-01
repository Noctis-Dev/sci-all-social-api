import pandas

from statsmodels.tsa.holtwinters import Holt
from web.dto.publication import PublicationPolarityResponse


def holt_models(data: PublicationPolarityResponse):
    models = {}
    for item in data.data:
        polarity_data = []
        for polarity in item.polarity:
            polarity_data.append({
                "date": polarity.date,
                "polarity": polarity.polarity
            })

        data_frame = pandas.DataFrame(polarity_data)
        data_frame['date'] = pandas.to_datetime(data_frame['date'])
        data_frame.set_index('date', inplace=True)

        data_frame = data_frame.asfreq('D')
        data_frame['polarity'].fillna(method='ffill', inplace=True)

        if len(data_frame) < 2:
            continue

        model = Holt(data_frame['polarity']).fit(smoothing_level=0.6, smoothing_slope=0.2)
        forecast = model.forecast(len(data_frame) // 2)

        models[item.publication_uuid] = forecast

    return models
