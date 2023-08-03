#pragma once
#include "rednose/helpers/common_ekf.h"
extern "C" {
void live_update_4(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_9(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_10(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_12(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_35(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_32(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_13(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_14(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_33(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_H(double *in_vec, double *out_2180208198623540544);
void live_err_fun(double *nom_x, double *delta_x, double *out_5908847586448158897);
void live_inv_err_fun(double *nom_x, double *true_x, double *out_6103806427594524617);
void live_H_mod_fun(double *state, double *out_1251961769881929919);
void live_f_fun(double *state, double dt, double *out_2234207053155067343);
void live_F_fun(double *state, double dt, double *out_2139475778566482604);
void live_h_4(double *state, double *unused, double *out_5452514281543858189);
void live_H_4(double *state, double *unused, double *out_6539003226263514649);
void live_h_9(double *state, double *unused, double *out_6681893194721717304);
void live_H_9(double *state, double *unused, double *out_6780192872893105294);
void live_h_10(double *state, double *unused, double *out_3077852986928858292);
void live_H_10(double *state, double *unused, double *out_7566935789090758089);
void live_h_12(double *state, double *unused, double *out_2403975194794623961);
void live_H_12(double *state, double *unused, double *out_6888284439414075172);
void live_h_35(double *state, double *unused, double *out_434714226688679640);
void live_H_35(double *state, double *unused, double *out_4142721407089061463);
void live_h_32(double *state, double *unused, double *out_5733829808833885505);
void live_H_32(double *state, double *unused, double *out_1437696894187311526);
void live_h_13(double *state, double *unused, double *out_6694347266348130037);
void live_H_13(double *state, double *unused, double *out_4269075578851257501);
void live_h_14(double *state, double *unused, double *out_6681893194721717304);
void live_H_14(double *state, double *unused, double *out_6780192872893105294);
void live_h_33(double *state, double *unused, double *out_1110723575095791883);
void live_H_33(double *state, double *unused, double *out_992164402450203859);
void live_predict(double *in_x, double *in_P, double *in_Q, double dt);
}