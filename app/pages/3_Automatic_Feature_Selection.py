import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn import linear_model
import numpy as np

from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV


st.header("Feature Selection Methods")

st.caption("How do we choose what variables we can introduce into our model?")

st.markdown(
    """
    There are plenty of ways or strategies how to select features. The most commonly used are the following:

    - Decide by computing the correlation coefficients between variables.
    - Use shrinkage methods like Ridge regression or Lasso regression.
    - Compute the variance inflation factor and sequentially remove those variables from the feature set.

    In order to demonstrate those methods, we will focus only on the rare type of collectables. The scope will not be a complete analysis, but just a small demonstation.
    """
)

# Initialize connection.
conn = st.experimental_connection('snowpark')

st.subheader("Correlation Matrix")

corr_query = "SELECT * FROM SORARE_ANALYSIS_RARE;"

result_corr = conn.query(corr_query, ttl=24*3600)#.drop(columns=["DISPLAY_NAME_PLAYER"])
result_corr.index = result_corr["DISPLAY_NAME_PLAYER"]
result_corr = result_corr.drop(columns=["DISPLAY_NAME_PLAYER","PRICE_MEAN"])

result_corr_diagram = result_corr.corr()

toggle_on = st.checkbox('Toggle correlation coefficient values in the boxes!')

st.caption("Make sure to expand the plotly diagram to see the values.")

if toggle_on:
    fig = px.imshow(result_corr_diagram, text_auto=True, color_continuous_scale='RdBu')
else: 
    fig = px.imshow(result_corr_diagram, color_continuous_scale='RdBu')

st.plotly_chart(fig)


# Rigde or Lasso

st.subheader("Ridge or Lasso?")

col1, col2 = st.columns(2)
with col1:
    r_o_l = st.selectbox("Choose method", ["Ridge", "Lasso"])
with col2:
    st.empty()

if r_o_l == "Ridge":
    X = result_corr.drop(columns=["PRICE_EUR_MEAN"])
    y = result_corr["PRICE_EUR_MEAN"]

    n_alphas = 200
    alphas = np.logspace(-5, 5, n_alphas)

    coefs = []

    for a in alphas:
        ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
        ridge.fit(X, y)
        coefs.append(ridge.coef_)

    ###Selecting lambda
    scaler=StandardScaler()
    X_std=scaler.fit_transform(X)

    ###Fit Ridge regression through cross validation
    regr_cv=RidgeCV(alphas=alphas)
    model_cv=regr_cv.fit(X_std,y)
    
    # fig_ridge, ax = plt.subplots()

    # PYPLOT
    # ax = plt.gca()

    # ax.plot(alphas, coefs)
    # ax.set_xscale("log")
    # ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
    # ax.set_xlabel("alpha")
    # ax.set_ylabel("weights")
    # ax.set_title("Ridge coefficients as a function of the regularization")
    # ax.legend(X.columns, loc = "lower center", bbox_to_anchor=(0.5, -0.6), fancybox=True, shadow=True, ncol=4)
    # ax.set_ylim(ymin=-250, ymax=1600)
    # #plt.xlabel("alpha")
    # #plt.ylabel("weights")
    # #plt.title("Ridge coefficients as a function of the regularization")
    # #plt.axis("tight")
    # #plt.show()
    # st.pyplot(fig_ridge)

    data = [ ]
    y_ = []

    for col in range(0, len(coefs[0])):
        y_.append([ ])
        for row in range(0, len(coefs)):
            y_[col].append(coefs[row][col])
            
    for i in range(0, len(y_)):
        trace = go.Scatter(y=y_[i], x=alphas,
                        mode='lines', showlegend=True, name=X.columns[i])
        data.append(trace)
        


    layout = go.Layout(title='Ridge coefficients as a function of the regularization',
                    hovermode='closest',
                    xaxis=dict(title='Alpha', type='log',
                                autorange='reversed'),
                    yaxis=dict(title='Weights'))
    
    
    fig = go.Figure(data=data, layout=layout)
    fig.add_vline(x=model_cv.alpha_, line_width=1.5, line_dash="dash", line_color="lightblue", name = "optimal alpha")

    st.plotly_chart(fig)

    st.markdown(
    """
    With the optimal alpha (blue dotted line) the optimal weights for the ridge regression could be used. With does weights a predition from the Linear Regression would be more precise than without the regularization method.
    Keep in mind, the optimal alpha was computed with Cross Validation. Still, there a lot of improvements possible. Especially the Cross Validation methods and it's parameters could be investigated more intensively.

    For this scope it is enough to get a feeling about the behaviour of the ridge regression with varying regularization parameter alpha.

    By the way, the greater the absoulte weight is, the more important is the feature for the Linear Regression results.

    One could think about to exclude all parameters, where the weights are very close to zero, in order to narrow down the feature selection.
    Yet, it is sufficient enough for this application here. Check out the Lasso Computation and it's interpretation.
    """
    )

if r_o_l == "Lasso":

    X = result_corr.drop(columns=["PRICE_EUR_MEAN"])
    y = result_corr["PRICE_EUR_MEAN"]

    scaler=StandardScaler()
    X_std=scaler.fit_transform(X)

    n_alphas = 100
    alphas = np.logspace(-3, 3, n_alphas)

    lasso = Lasso(max_iter=100)
    coefs = []

    for a in alphas:
        lasso.set_params(alpha=a)
        lasso.fit(X_std, y)
        coefs.append(lasso.coef_)


    model = LassoCV(cv=5, random_state=0, max_iter=100)

    # Fit model
    model.fit(X_std, y)

    data = [ ]
    y_ = []

    for col in range(0, len(coefs[0])):
        y_.append([ ])
        for row in range(0, len(coefs)):
            y_[col].append(coefs[row][col])
            
    for i in range(0, len(y_)):
        trace = go.Scatter(y=y_[i], x=alphas,
                        mode='lines', showlegend=True, name=X.columns[i])
        data.append(trace)
        


    layout = go.Layout(title='Lasso coefficients as a function of the regularization',
                    hovermode='closest',
                    xaxis=dict(title='Alpha', type='log',
                                autorange='reversed'),
                    yaxis=dict(title='Weights'))
    
    
    fig = go.Figure(data=data, layout=layout)
    fig.add_vline(x=model.alpha_, line_width=1.5, line_dash="dash", line_color="lightblue", name = "optimal alpha")

    st.plotly_chart(fig)

    opt_lasso_model = Lasso(max_iter=100, alpha=model.alpha_)
    opt_lasso_model.fit(X_std, y)

    show_coeff_lasso = st.checkbox('Toggle optimal Lasso coefficients as a dataframe!')

    if show_coeff_lasso:
        st.dataframe(opt_lasso_model.coef_)

    save = np.argwhere(opt_lasso_model.coef_== 0)

    removed_features = X.columns[save]

    st.markdown(f"Following features have been identified by Lasso, to be removed from the feature set:\n \n- {removed_features[0][0]}\n\n- {removed_features[1][0]} \n\n These variables turned out to result in a zero coefficient and thus should be removed. \n Although for this part the analysis reached the end, the feature selection work is not done yet. As further correlation matrices should be computed and analyzed as well. One should be advised to also calculate the variance inflation factor in order to further narrow down the feature set.\n\nBut for simple demonstration purposes, this should be it for now."
    )

    

