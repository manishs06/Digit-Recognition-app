from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
iris=load_iris()
x=iris.data
y=iris.target
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)
#load the model
model=LogisticRegression()
model.fit(x_train,y_train)
pickle.dump(model,open('model.pkl','wb'))
y_pred=model.predict(x_test)
accuracy_score=accuracy_score(y_test,y_pred)
print(accuracy_score)
