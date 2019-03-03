
%重力加速度****************************************************************
gravity = [0;0;-9.80665];  %重力加速度
g = 9.80665;
% 被者者データ    ""A""    ************************************************
height = SampleDataA(1,1);   %身長
A_weight = SampleDataA(1,2);    %体重59.8kg
A_foot_length = SampleDataA(1,3);   %足長さ
A_leg_length = SampleDataA(1,4);    %下腿長さ
A_thigh_length = SampleDataA(1,5) ;  %大腿長さ
A_torso_length = SampleDataA(1,6);  %胴長さ
A_head_length = SampleDataA(1,7);    %頭長さ
%arm_length = ave_arm_length;    %上腕長さ
%forearm_length = ave_forearm_length; %前腕長さ
%hand_length = ave_hand_length;   %手長さ
%l_length = l_length + 0.01;
%r_length = r_length + 0.01;
%慣性テンソル推定*******************************************************
A_foot_inertia = zeros(3,3);
    A_foot_inertia(1,1) = (-38.9258 + 214.578*A_foot_length + 0.01445*A_weight)/10000;
    A_foot_inertia(2,2) = (-6.29702 + 37.6738*A_foot_length + 0.01248*A_weight)/10000;
    A_foot_inertia(3,3) = (-40.9844 + 228.138*A_foot_length + 0.00753*A_weight)/10000;
A_leg_inertia = zeros(3,3);
    A_leg_inertia(1,1) = (-1190.24 + 3093.33*A_leg_length + 5.27481*A_weight)/10000;
    A_leg_inertia(2,2) = (-1174.66 + 3048.1 *A_leg_length + 5.19169*A_weight)/10000;
    A_leg_inertia(3,3) = (-62.7928 + 104.746*A_leg_length + 1.10838*A_weight)/10000;
A_thigh_inertia = zeros(3,3);
    A_thigh_inertia(2,2) = (-2043.38 + 5547.75*A_thigh_length + 10.6498*A_weight)/10000;
    A_thigh_inertia(3,3) = (-350.308 + 418.338*A_thigh_length + 6.6271 *A_weight)/10000;
A_torso_inertia = zeros(3,3);
    A_torso_inertia(1,1) = (-6157.42  + 15247.8*A_torso_length*(1-163/592) + 58.0109*A_weight)/10000;
    A_torso_inertia(2,2) = (-6423.4   + 15063.0*A_torso_length*(1-163/592) + 71.5226*A_weight)/10000;
    A_torso_inertia(3,3) = (-2016.55  - 1516.61*A_torso_length*(1-163/592) + 48.8973*A_weight)/10000;
%torso_inertia(1,1) = (-25180.2 + 43095.5*torso_length + 200.723*A_weight)/10000;
%torso_inertia(2,2) = (-25902.6 + 43759.1*torso_length + 217.775*A_weight)/10000;
%torso_inertia(3,3) = (-2482.2  -385.282*torso_length + 83.2293*A_weight)/10000;

A_pelvis_inertia = zeros(3,3);
 A_pelvis_inertia(1,1) = (-1687.06 + 5588.38*A_torso_length*163/592 + 22.6268*A_weight)/10000;
 A_pelvis_inertia(2,2) = (-1982.55 + 6516.01*A_torso_length*163/592 + 27.7046*A_weight)/10000;
 A_pelvis_inertia(3,3) = (-1376.85 - 2246.6 *A_torso_length*163/592 + 29.075 *A_weight)/10000;
%{
arm_inertia = zeros(3,3);
arm_inertia(1,1) = (-317.679 + 1007.85*arm_length + 1.85249*A_weight)/10000;
arm_inertia(2,2) = (-312.14 + 999.691*arm_length + 1.74277*A_weight)/10000;
arm_inertia(3,3) = (-11.1029 -44.8794*arm_length + 0.71203*A_weight)/10000;
forearm_inertia = zeros(3,3);
forearm_inertia(1,1) = (-145.867 + 562.219*forearm_length + 0.85722*A_weight)/10000;
forearm_inertia(2,2) = (-146.449 + 576.661*forearm_length + 0.79727*A_weight)/10000;
forearm_inertia(3,3) = (-13.4756 + 26.3785*forearm_length + 0.24644*A_weight)/10000;
hand_inertia = zeros(3,3);
hand_inertia(1,1) = (-6.36541 + 80.3581*hand_length + 0.10995*A_weight)/10000;
hand_inertia(2,2) = (-7.30695 + 82.0684*hand_length + 0.14433*A_weight)/10000;
hand_inertia(3,3) = (-1.67255 + 9.0812*hand_length + 0.05381*A_weight)/10000;
%}
A_head_inertia = zeros(3,3);
    A_head_inertia(1,1) = (-367.903 + 2843.24*A_head_length + 2.71413*A_weight)/10000;
    A_head_inertia(2,2) = (-354.077 + 2680.71*A_head_length + 2.4924*A_weight)/10000;
    A_head_inertia(3,3) = (-138.956 + 1307.37*A_head_length + 1.24856*A_weight)/10000;
    
display(A_head_inertia);
display(A_torso_inertia);
display(A_thigh_inertia);
%体節質量推定**************************************************************
A_foot_weight     =  -0.26784 + 2.61804*A_foot_length  + 0.00545*A_weight;
A_leg_weight      =  -1.71524 + 6.04396*A_leg_length   + 0.03885*A_weight;
A_thigh_weight    =  -4.53542 + 14.5253*A_thigh_length + 0.09324*A_weight;
A_pelvis_weight   = (-10.1647 + 18.7503*A_torso_length + 0.48275*A_weight) * (163/592);%座位時の肩峰高/超骨稜高
A_head_weight     =  -1.1968  + 25.9526*A_head_length  + 0.02604*A_weight;
A_torso_weight    = A_weight-(A_foot_weight+A_leg_weight+A_thigh_weight)*2-A_pelvis_weight-A_head_weight;
%arm_weight = -0.36785 + 1.15588*arm_length + 0.02712*A_weight;
%forearm_weight = -0.43807 + 2.22923*forearm_length + 0.01397*A_weight;
%hand_weight = -0.01474 + 2.09424*hand_length + 0.00414*A_weight;
%A_torso_weight = (-10.1647 + 18.7503*torso_length + 0.48275*A_weight) * 0.43/0.54;
%マーカ位置読み込み(必要なものだけ)**********************************************
% marker_name(1=x:2=y:3=z,1,k) = marker_position(k,marker_number * 1→3:2→3+1:3→3+2)/1000
%1000で割るのは単位をmmからmに変換するため
A_headF=zeros([3,1,analysis_frame]);A_headR=zeros([3,1,analysis_frame]);
A_headD=zeros([3,1,analysis_frame]);A_headT=zeros([3,1,analysis_frame]);
A_C7=zeros([3,1,analysis_frame]);  A_neckF=zeros([3,1,analysis_frame]);
A_R_ill=zeros([3,1,analysis_frame]);A_L_ill=zeros([3,1,analysis_frame]);
A_R_asis=zeros([3,1,analysis_frame]);A_L_asis=zeros([3,1,analysis_frame]);
A_Sacral=zeros([3,1,analysis_frame]);A_C_asis=zeros([3,1,analysis_frame]);
A_R_knee_out=zeros([3,1,analysis_frame]);A_R_knee_in=zeros([3,1,analysis_frame]);
A_R_ankle_out=zeros([3,1,analysis_frame]);A_R_ankle_in=zeros([3,1,analysis_frame]);
A_R_toe=zeros([3,1,analysis_frame]);A_R_heel=zeros([3,1,analysis_frame]);
A_R_shoulder=zeros([3,1,analysis_frame]);A_L_knee_out=zeros([3,1,analysis_frame]);
A_L_knee_in=zeros([3,1,analysis_frame]);A_L_ankle_out=zeros([3,1,analysis_frame]);
A_L_ankle_in=zeros([3,1,analysis_frame]);A_L_toe=zeros([3,1,analysis_frame]);
A_L_heel=zeros([3,1,analysis_frame]);A_L_shoulder=zeros([3,1,analysis_frame]);
A_R_elb=zeros([3,1,analysis_frame]);A_L_elb=zeros([3,1,analysis_frame]);
A_Body_R=zeros([3,1,analysis_frame]);A_Body_L=zeros([3,1,analysis_frame]);
for k = 1:analysis_frame
    %頭部位置同定
    A_headF(:,1,k) = A_Marker_Pos(k,1*3+0:1*3+2)/1000;%front
    A_headT(:,1,k) = A_Marker_Pos(k,2*3+0:2*3+2)/1000;%top
    A_headR(:,1,k) = A_Marker_Pos(k,3*3+0:3*3+2)/1000;%rear
    A_headD(:,1,k) = A_Marker_Pos(k,4*3+0:4*3+2)/1000;%dummy
    %体幹位置同定
    A_C7(:,1,k)         = A_Marker_Pos(k,5*3+0:5*3+2)/1000;
    A_neckF(:,1,k)      = A_Marker_Pos(k,6*3+0:6*3+2)/1000;
    A_R_shoulder(:,1,k) = A_Marker_Pos(k,7*3+0:7*3+2)/1000;
    A_L_shoulder(:,1,k) = A_Marker_Pos(k,8*3+0:8*3+2)/1000;
    A_R_elb(:,1,k)      = A_Marker_Pos(k,10*3+0:10*3+2)/1000;
    A_L_elb(:,1,k)      = A_Marker_Pos(k,12*3+0:12*3+2)/1000;
    A_Body_R(:,1,k)     = A_Marker_Pos(k,14*3+0:14*3+2)/1000;
    A_Body_L(:,1,k)     = A_Marker_Pos(k,16*3+0:16*3+2)/1000;
    %腰周り座標
    A_R_ill(:,1,k)    = A_Marker_Pos(k,17*3+0:17*3+2)/1000;
    A_L_ill(:,1,k)    = A_Marker_Pos(k,18*3+0:18*3+2)/1000;
    A_R_asis(:,1,k)   = A_Marker_Pos(k,19*3+0:19*3+2)/1000;
    A_L_asis(:,1,k)   = A_Marker_Pos(k,20*3+0:20*3+2)/1000;
    A_Sacral(:,1,k)   = A_Marker_Pos(k,21*3+0:21*3+2)/1000;
    %下肢位置同定
    A_R_knee_out(:,1,k)   = A_Marker_Pos(k,23*3+0:23*3+2)/1000;
    A_R_knee_in(:,1,k)    = A_Marker_Pos(k,24*3+0:24*3+2)/1000;
    A_R_ankle_out(:,1,k)  = A_Marker_Pos(k,25*3+0:25*3+2)/1000;
    A_R_ankle_in(:,1,k)   = A_Marker_Pos(k,26*3+0:26*3+2)/1000;
    A_R_heel(:,1,k)       = A_Marker_Pos(k,27*3+0:27*3+2)/1000;
    A_R_toe(:,1,k)        = A_Marker_Pos(k,28*3+0:28*3+2)/1000;
    A_L_knee_out(:,1,k)   = A_Marker_Pos(k,30*3+0:30*3+2)/1000;
    A_L_knee_in(:,1,k)    = A_Marker_Pos(k,31*3+0:31*3+2)/1000;
    A_L_ankle_out(:,1,k)  = A_Marker_Pos(k,32*3+0:32*3+2)/1000;
    A_L_ankle_in(:,1,k)   = A_Marker_Pos(k,33*3+0:33*3+2)/1000;
    A_L_heel(:,1,k)       = A_Marker_Pos(k,34*3+0:34*3+2)/1000;
    A_L_toe(:,1,k)        = A_Marker_Pos(k,35*3+0:35*3+2)/1000;
    %関節中心座標の準備
    A_cervical_JC     = (A_C7+A_neckF)/2;            %首原点
    A_C_asis(:,1,k)   = (A_R_asis(:,1,k)+A_L_asis(:,1,k))/2;
    A_uH2(:,1,k)      = A_R_asis(:,1,k)-A_C_asis(:,1,k);
    A_uH1(:,1,k)      = A_Sacral(:,1,k)-A_C_asis(:,1,k);
    A_uH3(:,1,k)      = cross(A_uH1(:,1,k),A_uH2(:,1,k));
    A_R_hip_JC(:,1,k) = A_C_asis(:,1,k)+0.64*A_uH2(:,1,k)+0.44*A_uH1(:,1,k)-0.68*A_uH3(:,1,k);
    A_L_hip_JC(:,1,k) = A_C_asis(:,1,k)-0.64*A_uH2(:,1,k)+0.44*A_uH1(:,1,k)-0.68*A_uH3(:,1,k);
    A_R_knee_JC       = (A_R_knee_out+A_R_knee_in)/2;
    A_L_knee_JC       = (A_L_knee_out+A_L_knee_in)/2;
    A_R_ankle_JC      = (A_R_ankle_out+A_R_ankle_in)/2;
    A_L_ankle_JC      = (A_L_ankle_out+A_L_ankle_in)/2;

end
A_Hip=(A_R_hip_JC+A_L_hip_JC)/2;
%絶対座標系基底ベクトル*************************************************************
abs_x=zeros([3,1,analysis_frame]);
abs_y=zeros([3,1,analysis_frame]);
abs_z=zeros([3,1,analysis_frame]);
for k=1:analysis_frame
    abs_x(1,1,k)=1;
    abs_y(2,1,k)=1;
    abs_z(3,1,k)=1;
end
%腰回転中心算出*******************************************************************
%相対座標(腰回転中心算出用)************************************************************
    A_C_ill = (A_R_ill+A_L_ill)/2;           %上前腸骨稜
for k=1:analysis_frame
    A_ur = A_R_asis-(A_R_ill+A_L_ill)/2;
    A_ul = A_L_asis-(A_R_ill+A_L_ill)/2;
%腰ジョイント用座標系xyz軸**********************************************************
    A_pel_z_axis(:,1,k) = basisvector2(A_ur(:,1,k),A_ul(:,1,k));
    A_pel_x_axis(:,1,k) = basisvector1(A_R_asis(:,1,k)/2-A_L_asis(:,1,k)/2);
    A_pel_y_axis(:,1,k) = basisvector2(A_pel_z_axis(:,1,k),A_pel_x_axis(:,1,k));
    A_pelvis_z_axis(:,1,k) = basisvector2(A_R_asis(:,1,k)-A_Sacral(:,1,k),A_L_asis(:,1,k)-A_Sacral(:,1,k));
    A_pelvis_x_axis(:,1,k) = basisvector1(A_R_ill(:,1,k)-A_C_ill(:,1,k));
    A_pelvis_y_axis(:,1,k) = basisvector2(A_pelvis_z_axis(:,1,k),A_pelvis_x_axis(:,1,k));
end

for k=1:analysis_frame
    A_pelvis_length(k)=basislength1(A_C_ill(:,1,k)-A_C_asis(:,1,k));
    A_waist_JC(:,:,k) = A_C_ill(:,:,k)-A_pelvis_length(k)*A_pelvis_y_axis(:,:,k)-0.5*A_pelvis_length(k)*A_pelvis_z_axis(:,:,k);       %腰回転中心L4/L5
end

%相対座標(胸)***************************************************************
for k=1:analysis_frame
    A_thorax_z_axis(:,1,k) = basisvector1(A_cervical_JC(:,1,k)-A_Hip(:,1,k));
    temp_A_thorax_x_axis(:,1,k) = basisvector1(A_R_shoulder(:,1,k)-A_L_shoulder(:,1,k));
    A_thorax_y_axis(:,1,k) = basisvector2(A_thorax_z_axis(:,1,k),temp_A_thorax_x_axis(:,1,k));
    A_thorax_x_axis(:,1,k) = basisvector2(A_thorax_y_axis(:,1,k),A_thorax_z_axis(:,1,k));
end
%相対座標(頭)****************************************************************
for k=1:analysis_frame
    A_head_z_axis(:,1,k) = basisvector1(A_headT(:,1,k)-(A_headF(:,1,k)+A_headR(:,1,k))/2);
    temp_A_head_x_axis(:,1,k) = basisvector1(A_headD(:,1,k)-(A_headF(:,1,k)+A_headR(:,1,k))/2);
    A_head_y_axis(:,1,k) = basisvector2(temp_A_head_x_axis(:,1,k),A_head_z_axis(:,1,k));
    A_head_x_axis(:,1,k) = basisvector2(A_head_y_axis(:,1,k),A_head_z_axis(:,1,k));
end
%相対座標(首)*******************************************************************
for k=1:analysis_frame
    A_cervical_z_axis(:,1,k) = basisvector1(A_cervical_JC(:,1,k)-A_waist_JC(:,1,k));
    temp_A_cervical_y_axis(:,1,k) = basisvector1(A_neckF(:,1,k)-A_C7(:,1,k));
    A_cervical_x_axis(:,1,k) = basisvector2(temp_A_cervical_y_axis(:,1,k),A_cervical_z_axis(:,1,k));
    A_cervical_y_axis(:,1,k) = basisvector2(A_cervical_z_axis(:,1,k),A_cervical_x_axis(:,1,k));
end
%相対座標(胴)*******************************************************************
for k=1:analysis_frame
    A_torso_x_axis(:,1,k) = basisvector1(A_Body_R(:,1,k)-A_Body_L(:,1,k));
    A_torso_z_axis(:,1,k) = basisvector1(A_cervical_JC(:,1,k)-A_waist_JC(:,1,k));
    A_torso_y_axis(:,1,k) = basisvector2(A_torso_z_axis(:,1,k),A_torso_x_axis(:,1,k));
%    A_torso_y_axis(:,1,k) = basisvector2(A_cervical_JC(:,1,k)-A_waist_JC(:,1,k),A_torso_x_axis(:,1,k));
%    A_torso_z_axis(:,1,k) = basisvector2(A_torso_x_axis(:,1,k),A_torso_y_axis(:,1,k));
%相対座標(右大腿=右膝)********************************************************
%相対座標(右下腿=右足)********************************************************
    A_R_thigh_z_axis(:,1,k) = basisvector1(A_R_hip_JC(:,1,k)-A_R_knee_JC(:,1,k));
    A_R_thigh_y_axis(:,1,k) = basisvector2(A_R_thigh_z_axis(:,1,k),A_R_knee_out(:,1,k)-A_R_knee_JC(:,1,k));
    A_R_thigh_x_axis(:,1,k) = basisvector2(A_R_thigh_y_axis(:,1,k),A_R_thigh_z_axis(:,1,k));
    A_R_leg_z_axis(:,1,k) = basisvector1(A_R_knee_JC(:,1,k)-A_R_ankle_JC(:,1,k));
    A_R_leg_y_axis(:,1,k) = basisvector2(A_R_leg_z_axis(:,1,k),A_R_ankle_out(:,1,k)-A_R_ankle_JC(:,1,k));
    A_R_leg_x_axis(:,1,k) = basisvector2(A_R_leg_y_axis(:,1,k),A_R_leg_z_axis(:,1,k));
%相対座標(右足)********************************************************
    A_R_foot_y_axis(:,1,k) = basisvector1(A_R_toe(:,1,k)-A_R_heel(:,1,k));
    A_R_foot_x_axis(:,1,k) = basisvector2(A_R_foot_y_axis(:,1,k),(A_R_ankle_JC(:,1,k)-A_R_heel(:,1,k)));
    A_R_foot_z_axis(:,1,k) = basisvector2(A_R_foot_x_axis(:,1,k),A_R_foot_y_axis(:,1,k));
%相対座標(左大腿=左膝)********************************************************
%相対座標(左下腿=左足)********************************************************
    A_L_thigh_z_axis(:,1,k) = basisvector1(A_L_hip_JC(:,1,k)-A_L_knee_JC(:,1,k));
    A_L_thigh_y_axis(:,1,k) = basisvector2(A_L_thigh_z_axis(:,1,k),A_L_knee_JC(:,1,k)-A_L_knee_out(:,1,k));
    A_L_thigh_x_axis(:,1,k) = basisvector2(A_L_thigh_y_axis(:,1,k),A_L_thigh_z_axis(:,1,k));
    A_L_leg_z_axis(:,1,k) = basisvector1(A_L_knee_JC(:,1,k)-A_L_ankle_JC(:,1,k));
    A_L_leg_y_axis(:,1,k) = basisvector2(A_L_leg_z_axis(:,1,k),A_L_ankle_JC(:,1,k)-A_L_ankle_out(:,1,k));
    A_L_leg_x_axis(:,1,k) = basisvector2(A_L_leg_y_axis(:,1,k),A_L_leg_z_axis(:,1,k));

%相対座標(左足)********************************************************
    A_L_foot_y_axis(:,1,k) = basisvector1(A_L_toe(:,1,k)-A_L_heel(:,1,k));
    A_L_foot_x_axis(:,1,k) = basisvector2(A_L_foot_y_axis(:,1,k),(A_L_ankle_JC(:,1,k)-A_L_heel(:,1,k)));
    A_L_foot_z_axis(:,1,k) = basisvector2(A_L_foot_x_axis(:,1,k),A_L_foot_y_axis(:,1,k));
    
    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%重心位置**********************************************************************
%for k=1:analysis_frame
    A_head_cog      = (17.9*A_cervical_JC + 82.1*A_headT)/100;
%    A_head_cog     = (50*A_headF + 50*A_headR)/100;
    A_torso_cog     = (50*A_C_ill + 50*A_cervical_JC)/100;
    A_pelvis_cog    = (50*A_C_ill + 50*(A_R_hip_JC + A_L_hip_JC)/2)/100;
    A_R_thigh_cog   = (52.5*A_R_hip_JC + 47.5*A_R_knee_JC)/100;
    A_L_thigh_cog   = (52.5*A_L_hip_JC + 47.5*A_L_knee_JC)/100;
    A_R_leg_cog     = (59.4*A_R_knee_JC + 40.6*A_R_ankle_JC)/100;
    A_L_leg_cog     = (59.4*A_L_knee_JC + 40.6*A_L_ankle_JC)/100;
    A_R_foot_cog    = A_R_heel + A_R_foot_y_axis * A_foot_length * 40.5/100;
    A_L_foot_cog    = A_L_heel + A_L_foot_y_axis * A_foot_length * 40.5/100;
%end
%重心速度**********************************************************************
%初期値を0とする
velo_A_head_cog(:,1,1)    =[0;0;0];
velo_A_torso_cog(:,1,1)   =[0;0;0];
velo_A_pelvis_cog(:,1,1)  =[0;0;0];
velo_A_R_thigh_cog(:,1,1) =[0;0;0];
velo_A_R_leg_cog(:,1,1)   =[0;0;0];
velo_A_R_foot_cog(:,1,1)  =[0;0;0];
velo_A_L_thigh_cog(:,1,1) =[0;0;0];
velo_A_L_leg_cog(:,1,1)   =[0;0;0];
velo_A_L_foot_cog(:,1,1)  =[0;0;0];
for k=2:analysis_frame
    velo_A_head_cog(:,1,k)    =(A_head_cog(:,1,k)   -A_head_cog(:,1,k-1))     *f_motion;
    velo_A_torso_cog(:,1,k)   =(A_torso_cog(:,1,k)  -A_torso_cog(:,1,k-1))    *f_motion;
    velo_A_pelvis_cog(:,1,k)  =(A_pelvis_cog(:,1,k) -A_pelvis_cog(:,1,k-1))   *f_motion;
    velo_A_R_thigh_cog(:,1,k) =(A_R_thigh_cog(:,1,k)-A_R_thigh_cog(:,1,k-1))  *f_motion;
    velo_A_R_leg_cog(:,1,k)   =(A_R_leg_cog(:,1,k)  -A_R_leg_cog(:,1,k-1))    *f_motion;
    velo_A_R_foot_cog(:,1,k)  =(A_R_foot_cog(:,1,k) -A_R_foot_cog(:,1,k-1))   *f_motion;
    velo_A_L_thigh_cog(:,1,k) =(A_L_thigh_cog(:,1,k)-A_L_thigh_cog(:,1,k-1))  *f_motion;
    velo_A_L_leg_cog(:,1,k)   =(A_L_leg_cog(:,1,k)  -A_L_leg_cog(:,1,k-1))    *f_motion;
    velo_A_L_foot_cog(:,1,k)  =(A_L_foot_cog(:,1,k) -A_L_foot_cog(:,1,k-1))   *f_motion;    
end
%重心加速度***************************************************************
%初期値を0とする
accel_A_head_cog(:,1,1)    =[0;0;0];
accel_A_torso_cog(:,1,1)   =[0;0;0];
accel_A_pelvis_cog(:,1,1)  =[0;0;0];
accel_A_R_thigh_cog(:,1,1) =[0;0;0];
accel_A_R_leg_cog(:,1,1)   =[0;0;0];
accel_A_R_foot_cog(:,1,1)  =[0;0;0];
accel_A_L_thigh_cog(:,1,1) =[0;0;0];
accel_A_L_leg_cog(:,1,1)   =[0;0;0];
accel_A_L_foot_cog(:,1,1)  =[0;0;0];
for k=2:analysis_frame
    accel_A_head_cog(:,1,k)    =(velo_A_head_cog(:,1,k)   -velo_A_head_cog(:,1,k-1))    *f_motion;
    accel_A_torso_cog(:,1,k)   =(velo_A_torso_cog(:,1,k)  -velo_A_torso_cog(:,1,k-1))   *f_motion;
    accel_A_pelvis_cog(:,1,k)  =(velo_A_pelvis_cog(:,1,k) -velo_A_pelvis_cog(:,1,k-1))  *f_motion;
    accel_A_R_thigh_cog(:,1,k) =(velo_A_R_thigh_cog(:,1,k)-velo_A_R_thigh_cog(:,1,k-1)) *f_motion;
    accel_A_R_leg_cog(:,1,k)   =(velo_A_R_leg_cog(:,1,k)  -velo_A_R_leg_cog(:,1,k-1))   *f_motion;
    accel_A_R_foot_cog(:,1,k)  =(velo_A_R_foot_cog(:,1,k) -velo_A_R_foot_cog(:,1,k-1))  *f_motion;
    accel_A_L_thigh_cog(:,1,k) =(velo_A_L_thigh_cog(:,1,k)-velo_A_L_thigh_cog(:,1,k-1)) *f_motion;
    accel_A_L_leg_cog(:,1,k)   =(velo_A_L_leg_cog(:,1,k)  -velo_A_L_leg_cog(:,1,k-1))   *f_motion;
    accel_A_L_foot_cog(:,1,k)  =(velo_A_L_foot_cog(:,1,k) -velo_A_L_foot_cog(:,1,k-1))  *f_motion;    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%角速度ベクトル_絶対座標**********************************************************
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%座標変換のための行列を定義
A_head_A=zeros([3,3,analysis_frame]);A_thorax_A=zeros([3,3,analysis_frame]);
A_torso_A=zeros([3,3,analysis_frame]);A_pelvis_A=zeros([3,3,analysis_frame]);
A_R_thigh_A=zeros([3,3,analysis_frame]);A_L_thigh_A=zeros([3,3,analysis_frame]);
A_R_leg_A=zeros([3,3,analysis_frame]);A_L_leg_A=zeros([3,3,analysis_frame]);
A_R_foot_A=zeros([3,3,analysis_frame]);A_L_foot_A=zeros([3,3,analysis_frame]);
%座標変換行列(頭)****************************************************************
for k=1:analysis_frame
A_head_A(:,1,k)   =A_head_x_axis(:,1,k);    A_head_A(:,2,k)   =A_head_y_axis(:,1,k);    A_head_A(:,3,k)   =A_head_z_axis(:,1,k);
A_torso_A(:,1,k)  =A_torso_x_axis(:,1,k);   A_torso_A(:,2,k)  =A_torso_y_axis(:,1,k);   A_torso_A(:,3,k)  =A_torso_z_axis(:,1,k);
A_pelvis_A(:,1,k) =A_pelvis_x_axis(:,1,k);  A_pelvis_A(:,2,k) =A_pelvis_y_axis(:,1,k);  A_pelvis_A(:,3,k) =A_pelvis_z_axis(:,1,k);
A_thorax_A(:,1,k) =A_thorax_x_axis(:,1,k);  A_thorax_A(:,2,k) =A_thorax_y_axis(:,1,k);  A_thorax_A(:,3,k) =A_thorax_z_axis(:,1,k);
A_R_thigh_A(:,1,k)=A_R_thigh_x_axis(:,1,k); A_R_thigh_A(:,2,k)=A_R_thigh_y_axis(:,1,k); A_R_thigh_A(:,3,k)=A_R_thigh_z_axis(:,1,k);
A_R_leg_A(:,1,k)  =A_R_leg_x_axis(:,1,k);   A_R_leg_A(:,2,k)  =A_R_leg_y_axis(:,1,k);   A_R_leg_A(:,3,k)  =A_R_leg_z_axis(:,1,k);
A_R_foot_A(:,1,k) =A_R_foot_x_axis(:,1,k);  A_R_foot_A(:,2,k) =A_R_foot_y_axis(:,1,k);  A_R_foot_A(:,3,k) =A_R_foot_z_axis(:,1,k);
A_L_thigh_A(:,1,k)=A_L_thigh_x_axis(:,1,k); A_L_thigh_A(:,2,k)=A_L_thigh_y_axis(:,1,k); A_L_thigh_A(:,3,k)=A_L_thigh_z_axis(:,1,k);
A_L_leg_A(:,1,k)  =A_L_leg_x_axis(:,1,k);   A_L_leg_A(:,2,k)  =A_L_leg_y_axis(:,1,k);   A_L_leg_A(:,3,k)  =A_L_leg_z_axis(:,1,k);
A_L_foot_A(:,1,k) =A_L_foot_x_axis(:,1,k);  A_L_foot_A(:,2,k) =A_L_foot_y_axis(:,1,k);  A_L_foot_A(:,3,k) =A_L_foot_z_axis(:,1,k);
end

%グローバル座標での書く速度ベクトルの算出
%1.変換行列の微分値を求める
%2.変換行列の転置を掛けてひずみ対象行列を算出
%3.三次元の角速度ベクトルを取り出す
A_head_ST=zeros([3,3,analysis_frame]);A_thorax_ST=zeros([3,3,analysis_frame]);A_torso_ST=zeros([3,3,analysis_frame]);
A_pelvis_ST=zeros([3,3,analysis_frame]);A_R_thigh_ST=zeros([3,3,analysis_frame]);A_R_leg_ST=zeros([3,3,analysis_frame]);
A_R_foot_ST=zeros([3,3,analysis_frame]);A_L_thigh_ST=zeros([3,3,analysis_frame]);A_L_leg_ST=zeros([3,3,analysis_frame]);
A_L_foot_ST=zeros([3,3,analysis_frame]);
%座標系をR(phi,theta,psi)であるとして、pitchのthetaを求めたい
A_torso_theta_d   =rpy_pitch(A_torso_A);
A_R_thigh_theta_d =rpy_pitch(A_R_thigh_A);
A_R_leg_theta_d   =rpy_pitch(A_R_leg_A);
A_L_thigh_theta_d =rpy_pitch(A_L_thigh_A);
A_L_leg_theta_d   =rpy_pitch(A_L_leg_A);
A_tunk_theta_d    =rpy_pitch(A_thorax_A);
