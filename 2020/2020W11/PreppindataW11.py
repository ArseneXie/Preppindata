import pandas as pd

xls = pd.ExcelFile("E:/PD 2020 Week 11 Input.xlsx")
order = pd.read_excel(xls,'Orders')
box = sorted(pd.read_excel(xls,'Box Sizes')['Box Size'].tolist(), reverse = True)
 
pack_detail = []        
for od in order.itertuples(index=False):
    remain = od[1]
    box_no = 0
    for b in box:
        while remain>=b:
            box_no = box_no + 1
            remain = remain - b
            pack_detail.append([od[0],od[1],box_no,b,b])
    if remain>0:
        box_no = box_no + 1
        pack_detail.append([od[0],od[1],box_no,b,remain])
soaps_per_box = pd.DataFrame(pack_detail, columns=['Order Number','Order Size','Box Number','Box Size','Soaps in Box'])

boxes_per_order = soaps_per_box.groupby(['Order Number','Order Size','Box Size'], as_index=False).agg({'Box Number':'count'})
boxes_per_order['Box Size'] = boxes_per_order['Box Size'].apply(lambda x: 'Boxes of '+str(x))
boxes_per_order = boxes_per_order.pivot_table(index=['Order Number','Order Size'],
                                              columns='Box Size', values='Box Number', aggfunc=sum).fillna(0)
boxes_per_order.reset_index(inplace=True)
