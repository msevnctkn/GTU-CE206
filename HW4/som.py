import numpy as np
from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as p
import matplotlib.text as text
from sympy.solvers import solve
from sympy import Symbol
import pandas as pd


class Buckling():
	def __init__(self, length = 5, MOIxx = 104 * 10 ** -6, MOIyy = 22.4 * 10 ** -6, Sigma_yield = 345 , A = 8560, E = 200 * 10 ** 9):
		"""Given Parameters"""
		self.length = length
		self.MOIxx = MOIxx
		self.MOIyy = MOIyy
		self.Sigma_yield = Sigma_yield
		self.A = A
		self.E = E


		"""Default Parameters"""
		self.n = 1 # Mode of Buckling

		"""
		Asked Parameters
		Length Of Effective
		The end of olumn is supported by fixed support. Therefore Le = 0.5 * L 
		"""
		self.Le = 0.5 * self.length

		print("Buckling of X-axis ", self.Critical_Load_xx(), "kN")
		print("Buckling of Y-axis ", self.Critical_Load_yy(), "kN")
		print("Yield Force ", self.Yield_Load(),"kN")
		print("Critical Load without Buckling or Yielding ", self.P_cr() / 1000 ,"kN\n\n")
		print("According to this result, the Column is to be yielding without buckling.\n\n")

	def Critical_Load_xx(self,):
		self.P_cr_x = ( (self.n) ** 2 * (pi) ** 2 * self.E * self.MOIxx ) / (self.Le) ** 2 		
		return round(self.P_cr_x / 1000, 3)

	def Critical_Load_yy(self):
		self.P_cr_y = ( (self.n) ** 2 * (pi) ** 2 * self.E * self.MOIyy ) / (self.Le) ** 2 		
		return round(self.P_cr_y / 1000, 3)
	

	def Yield_Load(self):
		self.F_yield = self.Sigma_yield * self.A
		return round(self.F_yield / 1000, 3)

	def P_cr(self):
		"""Determine the Minimum Force"""
		return min(self.P_cr_x, self.P_cr_y, self.F_yield)



som = Buckling()



class Truss:
	def __init__(self):
		
		self.Calculation()
		self.Plot()

	def Plot(self):
		fig = plt.figure()
		ax = fig.add_subplot()
		plt.axis("off")

		
		#Rectangle
		rect = plt.Rectangle((10,10), 18, 16, fc = "white" , ec = "blue", lw = 2.5)
		plt.gca().add_patch(rect)
		#plt.axis('scaled')
		plt.text(18, 9, "0.8L", size=10)
		plt.text(28.5, 18, "0.6L", size=10)

		#line
		x = [10,28]
		y = [10, 26]
		line = plt.Line2D(x,y, color="blue", linewidth= 2.5)
		ax.add_line(line)
		plt.text(9, 10, "A", size=16)
		plt.text(28, 26.25, "C", size=16)
		plt.text(18, 18, "L", size=10)


		#circle for roller support
		r = .3
		circle = plt.Circle((10, 10 - r), radius= r, fc = "blue" ,ec = "blue")
		plt.gca().add_patch(circle)
		plt.axis('scaled')
		rl_x = [9.25,10.75]
		rl_y = [10 - 2 * r, 10 - 2 * r]
		roller_line = plt.Line2D(rl_x, rl_y,color="blue")
		ax.add_line(roller_line)


		#triangle for pinned support
		l = 2
		points = np.array([[28,10], [28 - 2*r, 10 - 2*r], [28 + 2*r, 10 - 2*r]])
		polygon = p.Polygon(points, closed= False, color ="blue")
		plt.gca().add_patch(polygon)
		plt.text(28.1, 10, "B", size=16)
	

		#an arrow for Load P at Point D
		
		plt.arrow(10,26,-0.75,0, head_width=0.5, head_length= 0.5)
		plt.text(10, 26.25, "D", size=16)
		plt.text(7, 25.5, "5P", size=16)
		plt.show()



	def Calculation(self):

		#for By
		By = Symbol("By")
		Eq = 5 * 0.6 + By * 0.8
		By = solve(Eq)[0] 
		print("By: ",str(By) + "P")

		#for Ay
		Ay = Symbol("Ay")
		Eq2 = By + Ay
		Ay = solve(Eq2)[0]
		print("Ay: ", str(Ay) + "P")

		#for Bx
		Bx = Symbol("Bx")
		Eq3 = Bx - 5
		Bx = solve(Eq3)[0]
		print("Bx: ", str(Bx) + "P")

		#for Joint D
		F_DC = Symbol("F_DC")
		Eq4 = - 5 + F_DC
		F_DC = solve(Eq4)[0]
		print("F_DC: ", str(F_DC,) + "P")

		F_DA = Symbol("F_DA")
		Eq5 = F_DA
		F_DA = solve(Eq5)[0]
		print("F_DA: ", str(F_DA,) + "P")

		#for Joint A
		alpha = degrees(atan(0.6/0.8))
		print("alpha: ", alpha, "degrees")
		F_AC = Symbol("F_AC")
		Eq6 = Ay + F_AC * (sin(radians(alpha)))
		F_AC = solve(Eq6)[0]
		print("F_AC: ", str(F_AC) + "P")

		F_AB = -1 * F_AC * cos(radians(alpha))
		print("F_AB: ", str(F_AB) + "P")

		#for Joint B
		F_BC = -1 * By
		print("F_BC: ", str(F_BC) + "P")



		print("""
			This all calculation for unit weigth of P
			""")

		#for By
		By_u = Symbol("By")
		Eq_u = 1 * 0.6 + By_u * 0.8
		By_u = solve(Eq_u)[0] 
		print("By: ",str(By) + "P")

		#for Ay
		Ay_u = Symbol("Ay")
		Eq2_u = By_u + Ay_u
		Ay_u = solve(Eq2_u)[0]
		print("Ay: ", str(Ay_u) + "P")

		#for Bx
		Bx_u = Symbol("Bx")
		Eq3_u = Bx_u - 1
		Bx_u = solve(Eq3_u)[0]
		print("Bx: ", str(Bx_u) + "P")

		#for Joint D
		F_DC_u = Symbol("F_DC")
		Eq4_u = - 1 + F_DC_u
		F_DC_u = solve(Eq4_u)[0]
		print("F_DC: ", str(F_DC_u) + "P")

		F_DA_u = Symbol("F_DA")
		Eq5_u = F_DA_u
		F_DA_u = solve(Eq5_u)[0]
		print("F_DA: ", str(F_DA_u) + "P")

		#for Joint A
		alpha = degrees(atan(0.6/0.8))
		
		F_AC_u = Symbol("F_AC")
		Eq6_u = Ay_u + F_AC_u * (sin(radians(alpha)))
		F_AC_u = solve(Eq6_u)[0]
		print("F_AC: ", str(F_AC_u) + "P")

		F_AB_u = -1 * F_AC_u * cos(radians(alpha))
		print("F_AB: ", str(F_AB_u) + "P")

		#for Joint B
		F_BC_u = -1 * By_u
		print("F_BC: ", str(F_BC_u) + "P")


	
		data = {
			"n": [F_AB_u, F_AC_u, F_DA_u, F_BC_u, F_DC_u],
			"N": [F_AB, F_AC, F_DA, F_BC, F_DC],
			"L": [0.8, 1, .6, .6, .8],
			"nNL": [
					F_AB_u * F_AB * 0.8,
					F_AC_u * F_AC * 1,
					F_DA_u * F_DA * .6,
					F_BC_u * F_BC * .6,
					F_DC_u * F_DC * .8
					]
		}
		print()
		print()
		index = ["AB", "AC", "DA", "BC", "DC"]
		dataframe = pd.DataFrame(data, index)
		print(dataframe)
		nNL = 0
		for result in data["nNL"]:
			nNL += result

		print("Total nNL value: ", nNL)
		print()
		

		displacement = str(nNL) + "PL/AE"
		print("Displacement",displacement)


t = Truss()
