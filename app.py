import streamlit as st
import pandas as pd
from urllib.request import urlopen
import json

st.title("DIU Result with CGPA")
st.text("A full result analysis with information of all courses and total cgpa.")
st.text("")

id = st.text_input("Enter your Student ID", placeholder="101-15-12345")
btn = st.button("Submit")


def main():
	s_sem = id.split("-")[0]
	s = int(s_sem)
	sum_points = 0
	sum_credit = 0
	result_dict = {
		"Semester": [],
		"Course": [],
		"Grade": [],
		"Grade Point": [],
		"Credit": []
	}
	count = 0
	for i in range(0,12):
		try:
			result_url = f"http://software.diu.edu.bd:8189/result?grecaptcha=&semesterId={s}&studentId={id}"
			response = urlopen(result_url)
			data_json = json.loads(response.read())
		except ValueError:
			st.error("Unable to fetch one of the result or Server is slow!", icon="🚨")
			st.info('Try after sometime!', icon="ℹ️")
			return
		# print("Semester:", s)
		for c in data_json:
			c_semyr = c["semesterName"] + "-" + str(c["semesterYear"])
			c_title = c["courseTitle"]
			c_grade = c["gradeLetter"]
			c_gp = c["pointEquivalent"]
			c_credit = c["totalCredit"]
			c_point = c_gp * c_credit

			result_dict["Semester"].append(c_semyr)
			result_dict["Course"].append(c_title)
			result_dict["Grade"].append(c_grade)
			result_dict["Grade Point"].append(round(c_gp,2))
			result_dict["Credit"].append(int(c_credit))
			
			sum_points += c_point
			sum_credit += c_credit
		count+=1
		if count==3:
			count=0
			s+=7
		s+=1
	cg = round(sum_points/sum_credit, 2)
	cg_text = "Total CGPA: "+ str(round(sum_points/sum_credit, 2))

	id_text = "##### ID: "+ id + " → Total Credits: "+str(int(sum_credit))

	df = pd.DataFrame.from_dict(result_dict)
	st.markdown(id_text)
	st.subheader(cg_text)
	st.dataframe(df.style.format({"Grade Point": "{:.2f}"}))
	df["Total Credits"] = ""
	df.at[0,"Total Credits"]= int(sum_credit)
	df["Total CGPA"] = ""
	df.at[0,"Total CGPA"]= cg
	csv = df.to_csv().encode('utf-8')
	st.download_button(
		"Download CSV",
		csv,
		f"{id}_result.csv",
		"text/csv",
		key='download-csv'
	)

	st.markdown("##")
	st.write("Copyright © 2022 Sajal Das. [[LinkedIn](https://www.linkedin.com/in/sajaldoes/)]")
	

if __name__ == '__main__' and id != "" or btn:
	main()
else:
	st.markdown("##")
	st.write("Copyright © 2022 Sajal Das. [[LinkedIn](https://www.linkedin.com/in/sajaldoes/)]")