import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression

iris=load_iris()
x=iris.data
y=iris.target
model=LinearRegression()
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.40,random_state=0)



model=pickle.load(open('model.pkl','rb'))
y_pred=model.predict(x_test)
accuracy=accuracy_score(y_test,y_pred)
print(accuracy)

