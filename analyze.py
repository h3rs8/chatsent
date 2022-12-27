from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt
import nltk
nltk.download('vader_lexicon')


def sentify(df):
    sent = SentimentIntensityAnalyzer()
    df['positive'] = [sent.polarity_scores(''.join(i))["pos"] for i in df["messages"]]
    df['negative'] = [sent.polarity_scores(''.join(i))["neg"] for i in df["messages"]]
    df['neutral'] = [sent.polarity_scores(''.join(i))["neu"] for i in df["messages"]]

    df['pos'] = df.apply(lambda x: 1 if x['positive'] > x['negative'] and x['positive'] > x['neutral'] else 0, axis=1)
    df['neg'] = df.apply(lambda x: 1 if x['negative'] > x['positive'] and x['negative'] > x['neutral'] else 0, axis=1)
    df['neu'] = df.apply(lambda x: 1 if x['neutral'] > x['negative'] and x['neutral'] > x['positive'] else 0, axis=1)

    dfzero = df[(df['pos'] == 0) & (df['neg'] == 0) & (df['neu'] == 0)]  # removing rows with pos = neg= neu = 0
    indx = dfzero[['pos', 'neg', 'neu']].index
    df.drop(indx, inplace=True)

    dfg = df.groupby('users', as_index=False).mean(numeric_only=True)

    # removing notification from users column
    ind = dfg[dfg['users'] == 'notification'].index
    dfg.drop(ind, inplace=True)
    return dfg


def names(df, num, typ):

    df.sort_values(typ, axis=0, ascending=False, inplace=True)
    dfa = df.head(num)
    lst = dfa['users'].unique().tolist()

    return lst


def plotchart(sizes, labels, colors):
    fig, ax = plt.subplots()
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, sizes, align='center', color=colors)
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Percentage')
    ax.set_title('Sentiment Analysis')
    ax.bar_label(bars)

    return fig


def remove_notifications(df):
    ind = df[df['users'] == 'notification'].index
    df.drop(ind, inplace=True)
    return df
