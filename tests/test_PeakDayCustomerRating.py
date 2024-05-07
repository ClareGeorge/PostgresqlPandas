import os

import pandas as pd
class TestPeakDayCustomerRating:

    def test_calculate_via_sql(self):
        df_1 = pd.read_sql("""select
	                        sum (case rating when 'Premium' then 1 else 0 end) as Premium,
	                        sum (case rating when 'Regular' then 1 else 0 end) as Regular,
	                        sum (case rating when 'Normal' then 1 else 0 end) as Normal
                            from ( select rating  from (select (case sum(amount)
                            when 9.98 then 'Premium'
							  				when 8.97 then 'Regular'
											else 'Normal'
							 			end) as Rating from payment where payment_date in (
										select  payment_date from payment
										group by payment_date
										order by count(*) desc
										limit 1
									)
								group by customer_id
								order by  sum(amount) desc	
				                    )
		                    )""", self.postgres_db_engine)
        with pd.ExcelWriter(os.getenv("peakday_file"),
                            mode='w',
                            engine="openpyxl",
                            ) as writer:
            df_1.to_excel(writer, sheet_name="SQL_PeakDayRating", header=True, index=False)

    def test_calculate_via_pandas(self):
        pay_df = pd.read_sql("select * from payment", self.postgres_db_engine)
        pay_df.groupby(['payment_date']).count()['customer_id'].sort_values(ascending=False)
        series_peakday = pay_df.groupby(['payment_date']).count()['customer_id'].sort_values(ascending=False).head(1)

        peakday = series_peakday.index[0]
        df_peakday_trans = pay_df[pay_df['payment_date'] == peakday]
        df_peakday_sum = df_peakday_trans.groupby("customer_id").sum(numeric_only=True)
        df_peakday_sum.rename(columns={'amount': "Total"}, inplace=True)
        cond = df_peakday_sum['Total'] == 9.98
        df_peakday_sum.loc[cond, ['Rating']] = ['Premium']
        cond = df_peakday_sum['Total'] == 8.97
        df_peakday_sum.loc[cond, ['Rating']] = ['Regular']
        cond = df_peakday_sum['Total'] <= 7.98
        df_peakday_sum.loc[cond, ['Rating']] = ['Normal']
        df_peakday_rating = df_peakday_sum.groupby('Rating').count()['payment_id'].sort_values(\
            ascending=False).to_frame().T
        df_peakday_rating = df_peakday_rating[['Premium', 'Regular', 'Normal']]
        df_peakday_rating.index = ["peak-day-customer"]
        with pd.ExcelWriter(os.getenv("peakday_file"),
                            mode='a',
                            engine="openpyxl",
                            ) as writer:
            df_peakday_rating.to_excel(writer, sheet_name="DataFrame_PeakDayRating", header=True, index=False)
