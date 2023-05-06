import streamlit as st
import streamlit.components.v1 as components

st.title("About this Project")

st.subheader("What does this project answer? How serious are those calculations and what is it for?")

st.write("""This project was created as an university project to demonstrate newly acquired skills
         in Machine Learning and Econometrics at Aix-Marseille University. All of the data is as of January 2022.
         Further it was queried from the Sorare API https://github.com/sorare/api 
         Thankfully, Sorare provided the data open source. This streamlit app shall represent my skills and be an example for my Data Science Portfolio of Projects. 
         The underlying database for the deployed app is stored at a Snowflake database, which is not publicly available.
         """)

st.subheader("About me!")

col1, col2, col3 = st.columns((1,0.5,4))

with col1:
    st.image("https://nenad-lelovic.de/css/img/person_img.jpg")
with col2:
    st.empty()
with col3:
    st.markdown(
        """
        My name is Nenad Lelovic and I am a Master Student at the University Konstanz and Université Aix-Marseille.
        I majored Econometrics, Big Data and Statistics as well as Quantitative Finance. In recent years I learned a lot in Software Engnineering and the theories behind Machine Learning and Probability Theory.

        If you like to [connect with me on LinkedIn](https://www.linkedin.com/in/nenad-lelovic/) feel free to send me an invite!
        """
    )

st.subheader("Disclaimer")

st.write("""Although the used models were used reasonably and seriously, the implications out of those results
         are not valid and outdated. The Streamlit app was created for weak informative purposes and
         never intends to incentivize doing investment decisions based on those results. All statements without guarantee.
         """)

st.subheader("Acknowledgments")

st.write(""" First, I want to thank Sorare for providing data open source. Without them, the whole Streamlit App and 
         the university project would not be a great success. So check the Website out at https://sorare.com/ . Further I want to thank University Konstanz and Aix-Marseille University for the high quality education.
         Special thanks to Ms. Lyudmila Grigoryeva and Mr. Winfried Pohlmeier for drastically improving my relevant hard skills. Last but not least, I want to thank Julia Funkner, Alexander Beales, Kevin Polaczek, Daniil Parfenov, Jelena Lelovic, and my parents 
         for all the assistance and happy times in my live. They deserve all the best.
         """)
