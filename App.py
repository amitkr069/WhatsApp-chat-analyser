import matplotlib.pyplot as plt
import streamlit as st
import preprocess, helper
import seaborn as sns
from zipfile import ZipFile

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload your chat zip file")
if uploaded_file is not None:
    if uploaded_file is not None:
        # Extracting the zip file
        with ZipFile(uploaded_file) as myzip:
            text_files = [f for f in myzip.namelist() if f.endswith('.txt') and f.startswith("WhatsApp")]
            if text_files:
                for file_name in text_files:
                    with myzip.open(file_name) as myfile:
                        # bytes_data = myfile.getvalue()
                        data = myfile.read().decode('utf-8')
                        # st.subheader(f"Content of {file_name}:")
                        # st.text(content)
            else:
                st.write("No text files found in the ZIP file.")
    # To read file as bytes:
    # bytes_data = uploaded_file.getvalue()

    #bytes ko string me convert krna hai
    # data = bytes_data.decode("utf-8")
    df = preprocess.preprocessor(data)

    #st.dataframe(df) #st.dataframe to print dataframe
    #st.text(data)

    st.header("Top Statistics")
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort() #sort in alphabetical order
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_medias, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_medias)
        with col4:
            st.header("Links Shared")
            st.title(links)


        #Monthly timeline
        timeline = helper.monthly_timeline(selected_user, df)
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color="lightgreen")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily_timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.title("Daily Timeline")
        fig1, ax1 = plt.subplots()
        #plt.figure(figsize=(15, 5))
        ax1.plot(daily_timeline['date_only'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)


        #Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #weekly heatmap
        st.title("Weekly activity Map")
        pivot = helper.activity_heatmap(selected_user, df)
        fig, ax2 = plt.subplots(figsize=(15,5))
        ax2 = sns.heatmap(pivot)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #now for most busy users

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        #Wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_words = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_words['word'], most_words['count'])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        #emoji
        emoji_df = helper.most_common_emoji(selected_user, df)
        st.title('Emoji Analysis')
        #st.dataframe(emoji_df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'], labels = emoji_df['emoji'], autopct = "%0.2f")
            st.pyplot(fig)
