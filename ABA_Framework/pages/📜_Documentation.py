import streamlit as st


st.set_page_config(
  page_title='Documentation',
  layout='wide',
  page_icon='📜'
)

st.sidebar.image("https://i.ibb.co/w4mGQk4/image-removebg-preview.png")

st.title('Documentation')

st.markdown("""
**ABA Generator**

This online application serves as an **ABA (Assumption-Based Argumentation)** generator designed for defining and managing argumentation frameworks. It was built in the context of the class project for M2 IA at Lyon 1 by the group comprised of Axel Colmant, Awated Edhib, Aida Haouas and Mohamed Massamba Sene.
            
The key features include:

1. **Language and Assumptions Definition:** Users can define literals, rules, and assumptions for the argumentation framework.
2. **Contraries Definition:** Contraries for each assumption can be specified to structure the argumentation model.
3. **Framework Conversion:** The application automatically converts the input into non-circular and atomic ABA frameworks for more efficient reasoning.
4. **Argument and Attack Generation:** It generates all possible arguments and attack relationships based on the defined rules and assumptions.
5. **Preference Handling:** Users can assign preferences between assumptions, and the application will compute normal and reverse attacks accordingly.

The application provides a user-friendly interface for constructing and exploring various ABA frameworks.
            
#### Expected Input Format
The format expected for the literals are as follows:
1. **Language**
            
The language literal is expected to be inputed in the format of comma separated values without space between the value such as in the examples below.
```
a,b,c,d
a,x,y,z
```     

2. **Assumptions**

The assumption literal is expected to be inputed in the format of comma separated values without space between the value such as in the examples below.
```
a,b,c
a
```                 

            
3. **Rules**
            
The rule literal is expected to input in the format of comma seperated tuples without space between the tuples. Each tuple being in the format (rule_head, rule_body) where if the body contains multiple values then it must also a tuple.
```
Given these set of rules
[r1]: p <- q,a
[r2]: q <- 
[r3]: r <- b       
The input should be as follows
(p,(q,a)),(q,),(r,b) 
```
            
4. **Contraries**
            
The contrary literal is expected to be inputed as comma sepated tuples without space between the tuple. Each tuple being in the format (contrary,argument).
```
Given these contaries
a_bar=r,b_bar=s
The input should be as follows
(a,r),(b,s)
```
            
5. **Preferences**

The preference literal is expected to input in the format of comma seperated tuples without space between the tuples. Each tuple being in the format (least_preferred, most_preferred) where if most_preferred contains multiple values then it must also a tuple.
```
Given these preference
a > b
c,d > e    
The input should be as follows
(b,a),(e,(c,d)) 
``` 

The below image show what the expected input looks like:
![Expected Input](https://i.postimg.cc/2SFDzJWN/Expected-Input.png)   

#### Loading class examples       
We provide a selectbox to enable users to load examples from TD4 as templates, all the user has to do is select amongst the options and provided and it will be loaded as can be seen in the below image. 
![Loading Example](https://i.postimg.cc/bYHWSbJ1/examples.png)
            
#### Usage
On the top row, we display three buttons: `Generate framework`, `Convert to atomic`, `Convert to non circular`
            
By clicking on the button corresponding to their use case, users can either generate the atomic, non-circular or base ABA framework corresponding to the inputted literals. The output will then be shown on the below text area.
            
The below example show cases the generation of the ABA framework.
            
![Generation Example](https://i.postimg.cc/PqSQYmcF/generate.png)
            
On the bottom row, we display three other buttons: `Create Arguments`, `Create Attacks`, `Create normal/reverse attacks`
            
By clicking on the button corresponding to their use case, a selectbox will appear where the user can choose to convert the framework to atomic, non-circular or apply no conversion before the create of arguments or attacks. The output will then be show on the below text area.
            
The below example show cases the computation of arguments for the ABA framework.

![Argument Example](https://i.postimg.cc/cCLqTM4g/arguments.png)
""")

