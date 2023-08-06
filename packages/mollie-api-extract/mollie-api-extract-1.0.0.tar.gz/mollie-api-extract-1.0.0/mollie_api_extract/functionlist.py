import requests
import pandas as pd
def mollie_payments(access_token, account_name='payments'):
    loop = 1
    df2 = pd.DataFrame()
    base_url = "https://api.mollie.com/v2/payments?limit=250" ##extract form postgres
    while loop==1:
        access_string = "Bearer " + access_token
        headers={"Authorization": access_string}
        response = requests.get(base_url, headers=headers)
        data = response.json()
        df1 = pd.DataFrame(data['_embedded']['payments'])

        ##optional fields coming (or not) from API : https://docs.mollie.com/reference/v2/payments-api/get-payment#response
        try:
            df1['is_cancellable']=df1['isCancelable']
        except:
            df1['is_cancellable']=None
        try:
            df1['authorized_at']=df1['authorizedAt']
        except:
            df1['authorized_at']=None
        try:
            df1['paid_at']=df1['paidAt']
        except:
            df1['paid_at']=None
        try:
            df1['expires_at']=df1['expiresAt']
        except:
            df1['expires_at']=None
        try:
            df1['expired_at']=df1['expiredAt']
        except:
            df1['expired_at']=None
        try:
            df1['webhook_url']=df1['webhookUrl']
        except:
            df1['webhook_url']=None
        try:
            df1['failed_at']=df1['failedAt']
        except:
            df1['failed_at']=None
        try:
            df1['amount_refunded'] = df1['amountRefunded'].apply(pd.Series)['value']
            df1['amount_refund_currency'] = df1['amountRefunded'].apply(pd.Series)['currency']
        except:
            df1['amount_refunded'] = None
            df1['amount_refund_currency'] = None
        try:
            df1['amount_remaining'] = df1['amountRemaining'].apply(pd.Series)['value']
            df1['amount_remaining_currency'] = df1['amountRemaining'].apply(pd.Series)['currency']
        except:
            df1['amount_remaining'] = None
            df1['amount_remaining_currency'] = None
        try:
            df1['amount_captured'] = df1['amountCaptured'].apply(pd.Series)['value']
            df1['amount_captured_currency'] = df1['amountCaptured'].apply(pd.Series)['currency']
        except:
            df1['amount_captured'] = None
            df1['amount_captured_currency'] = None
        try:
            df1['metadata_order_id'] = df1['metadata'].apply(pd.Series)['order_id']
            df1['metadata_refund_token'] = df1['metadata'].apply(pd.Series)['refund_token']
            df1['metadata_customer_id'] = df1['metadata'].apply(pd.Series)['customer_id']
        except:
            df1['metadata_order_id'] = None
            df1['metadata_refund_token'] = None
            df1['metadata_customer_id'] = None
        try:
            df1['restricted_to_country']=df1['restrictPaymentMethodsToCountry']
        except:
            df1['restricted_to_country']=None
        try:
            df1['country_code']=df1['countryCode']
        except:
            df1['country_code']=None
        try:
            df1['settlement_id']=df1['settlementId']
        except:
            df1['settlement_id']=None
        try:
            df1['customer_id']=df1['customerId']
        except:
            df1['customer_id']=None
        try:
            df1['mandate_id']=df1['mandateId']
        except:
            df1['mandate_id']=None
        try:
            df1['subscription_id']=df1['subscriptionId']
        except:
            df1['subscription_id']=None
        try:
            df1['order_id']=df1['orderId']
        except:
            df1['order_id']=None
        try:
            df1['application_fee_amount_value'] = df1['applicationFee']['amount'].apply(pd.Series)['value']
            df1['application_fee_amount_currency'] = df1['applicationFee']['amount'].apply(pd.Series)['currency']
            df1['application_fee_description'] = df1['applicationFee']['description']
        except:
            df1['application_fee_amount_value'] = None
            df1['application_fee_amount_currency'] = None
            df1['application_fee_description'] = None
        try:
            df1['settlement_amount'] = df1['settlementAmount'].apply(pd.Series)['value']
            df1['settlement_amount_currency'] = df1['settlementAmount'].apply(pd.Series)['currency']
        except:
            df1['settlement_amount'] = None
            df1['settlement_amount_currency'] = None
        df1['amount_value'] = df1['amount'].apply(pd.Series)['value']
        df1['amount_currency'] = df1['amount'].apply(pd.Series)['currency']
        df1['mollie_account'] = account_name
        df1['links']=df1['_links']
        df3 = df1[['mollie_account','profileId','resource','id','mode','createdAt','status',
        'amount_value','amount_currency','method','locale','sequenceType',
        'description','details','is_cancellable','authorized_at','paid_at',
        'expires_at','expired_at','failed_at','amount_refunded',
        'amount_refund_currency','amount_remaining','amount_remaining_currency','amount_captured',
        'amount_captured_currency','metadata','metadata_order_id','metadata_refund_token',
        'metadata_customer_id','restricted_to_country','country_code','settlement_id','customer_id','mandate_id',
        'subscription_id','order_id','application_fee_amount_value','application_fee_amount_currency',
        'application_fee_description','settlement_amount','settlement_amount_currency',
        'links','redirectUrl','webhook_url']]
        df2=pd.concat([df2, df3])
        nxt = data['_links']['next']
        if nxt!=None:
            nxt = data['_links']['next']['href']
            print("going to next API requests for 250 rows..")
            base_url=nxt
        else:
            loop=0
    return(df2)


def mollie_refunds(access_token,account_name='refunds'):
    loop = 1
    base_url = "https://api.mollie.com/v2/refunds?limit=250" ##extract form postgres
    while loop==1:
        access_string = "Bearer " + access_token
        headers={"Authorization": access_string}
        response = requests.get(base_url, headers=headers)
        data = response.json()
        df1 = pd.DataFrame(data['_embedded']['refunds'])
        df1['mollie_account'] = account_name
        df1['amount_value'] = df1['amount'].apply(pd.Series)['value']
        df1['amount_currency'] = df1['amount'].apply(pd.Series)['currency']
        nxt = data['_links']['next']
        if nxt!=None:
            nxt = data['_links']['next']['href']
            base_url=nxt
            loop=0
        else:
            loop=0
    return(df1)



def mollie_refund(payment_id, refund_id, access_token):
    base_url = "https://api.mollie.com/v2/payments/{}/refunds/{}".format(payment_id, refund_id)
    access_string = "Bearer " + access_token
    headers={"Authorization": access_string}
    response = requests.get(base_url, headers=headers)
    data = response.json()
    data=pd.DataFrame(data)
    return(data)



