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
	semesters = [191, 192, 193, 201, 202, 203, 211, 212, 213, 221, 222, 223]
	sum_points = 0
	sum_credit = 0
	result_dict = {
		"Semester": [],
		"Course": [],
		"Grade": [],
		"Grade Point": [],
		"Credit": []
	}
	for s in semesters:
		try:
			result_url = f"http://software.diu.edu.bd:8189/result?grecaptcha=&semesterId={s}&studentId={id}"
			response = urlopen(result_url)
			data_json = json.loads(response.read())
		except ValueError:
			st.write("Error occured or Server is slow!")
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

	cg = round(sum_points/sum_credit, 2)
	cg_text = "ID: "+ id + "     →      Total CGPA: "+ str(round(sum_points/sum_credit, 2))
	# id_text = 
	df = pd.DataFrame.from_dict(result_dict)
	# st.subheader(id_text)
	st.subheader(cg_text)
	st.dataframe(df.style.format({"Grade Point": "{:.2f}"}))
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