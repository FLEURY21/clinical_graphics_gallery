data WORK.adae;
	infile "C:\Users\FLEURYM\Desktop\VIGNETTES\CDISC_simulated_data\adae2.txt"
	dlm='09'x
	MISSOVER 
	DSD
	firstobs=2
	lrecl=32767;
input ID $ SUBJID $ ARM $ SEX $ AEBODSYS $ AETOXGR ;
run;

data WORK.ADAE;
	set WORK.ADAE;
	if ARM in ("A: Drug") then ARM = "Drug";
	else ARM = "Placebo";
RUN;


proc sql;
    create table df_pct as
    select 
        a.ARM,
        a.SEX,
        a.AEBODSYS,
        count(*) as n,
        calculated n / b.total as pct,
        put(calculated n / b.total * 100, 5.1) || '%' as pct_label
    from adae a
    inner join 
        (select ARM, SEX, count(*) as total
         from adae
         group by ARM, SEX) b
    on a.ARM = b.ARM and a.SEX = b.SEX
    group by a.ARM, a.SEX, a.AEBODSYS, b.total
    ;
quit;

data df_pct;
    set df_pct;
	length pct_label_ 8.;
    pct_label_ = round(pct*100, 0.01); 
run;


ods listing gpath='C:\Users\FLEURYM\Desktop\VIGNETTES\VIGNETTE_graphics\images' image_dpi=300 style=listing;
ods graphics / reset width=6in height=4in imagename='MOSAIC2';
proc sgpanel data=df_pct;
    panelby ARM / columns=2 novarname spacing=10;
    vbar SEX / response=pct_label_
               group=AEBODSYS
               stat=sum
               seglabel
               datalabelattrs=(weight=bold color=black size=12)
               outlineattrs=(thickness=1);
    rowaxis label="Pourcentage";
    keylegend / title="SOC";
	colaxis grid;
run;
ods graphics off;
ods listing close;





