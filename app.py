import streamlit as st
import pre
import analyze


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = pre.prepare(data)  # prepare the dataframe

    if "drop_down_selected" not in st.session_state:
        st.session_state.drop_down_selected = 'Select'

    if "btn1_clicked" not in st.session_state:
        st.session_state.btn1_clicked = False

    st.session_state.drop_down_selected = analysis_typ = st.sidebar.selectbox("Select type of analysis", ['Select', 'Positive', 'Negative', 'Neutral','Overall','Individual'])
    btn1 = st.sidebar.button("Get Analysis")
    ov = False
    if analysis_typ:
        if analysis_typ == 'Positive':
            typ = 'pos'
        elif analysis_typ == 'Negative':
            typ = 'neg'
        elif analysis_typ == 'Neutral':
            typ = 'neu'
        elif analysis_typ == 'Overall':
            typ = 'Overall'
        elif analysis_typ == 'Individual':
            typ = 'Individual'
        else:
            typ = 'Select'

        dfg = analyze.sentify(df)
        # df here gets updated to contain users,messages, postive, negative, neutral for each message and a 1 for pos neg or neu indicating the polarity of the message
        # whereas dfg shall contain the groupedby polarity of each user
        if typ == 'Select':
            btn1 = False
            st.session_state.btn1_clicked = False

        if btn1 or st.session_state.btn1_clicked:
            st.session_state.btn1_clicked = True
            if typ == 'Overall':
                st.header('Overall Analysis')

                labels = 'Positive', 'Negative', 'Neutral'
                dfa = analyze.remove_notifications(df.copy())

                sizes = float(dfa['pos'].mean()) * 100, float(dfa['neg'].mean()) * 100, float(dfa['neu'].mean()) * 100
                colors = ['yellowgreen', 'gold', 'lightskyblue']

                fig = analyze.plotchart(sizes, labels, colors)
                st.write("Most Active Person: "+str(dfa.groupby('users', as_index=False).count().sort_values("pos", axis =0, ascending=False).iloc[0]["users"])+", Messages: "+str(dfa.groupby('users', as_index=False).count().sort_values("pos", axis =0, ascending=False).iloc[0]["pos"]))
                st.pyplot(fig)
                #st.dataframe(dfa)

            elif typ == 'Individual':
                st.header("Select a name from the list to analyze individually")
                nam_list = list(dfg['users'])
                nam = st.selectbox("Select the person to analyze", nam_list)

                nam_sentiments = dfg[dfg['users'] == nam]

                labels = 'Positive', 'Negative', 'Neutral'
                sizes = float(nam_sentiments['pos']) * 100, float(nam_sentiments['neg']) * 100, float(
                    nam_sentiments['neu']) * 100
                colors = ['yellowgreen', 'gold', 'lightskyblue']

                fig = analyze.plotchart(sizes, labels, colors)
                st.pyplot(fig)

                #st.dataframe(dfg[dfg['users'] == nam])



            else:
                num = st.number_input(label='Number of users to be analyzed:',min_value=1,step=1)

                usr_list = analyze.names(dfg, num, typ)

                st.title('Most ' + analysis_typ + ' People Are:')
                st.write(', '.join(usr_list))
                usr = st.selectbox("Select the person to analyze", usr_list)
                if st.button("Analyze user"):
                    usr_sentiments = dfg[dfg['users'] == usr]



                    labels = 'Positive', 'Negative', 'Neutral'
                    sizes = float(usr_sentiments['pos'])*100, float(usr_sentiments['neg'])*100, float(usr_sentiments['neu'])*100
                    colors = ['yellowgreen', 'gold', 'lightskyblue']

                    fig = analyze.plotchart(sizes, labels , colors)
                    st.pyplot(fig)
                    #st.dataframe(usr_sentiments)
