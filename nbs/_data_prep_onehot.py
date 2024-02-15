import pandas as pd

def _role_str2list(df, col_name="role_description"):
    df[col_name] = df[col_name].str.split("Gazing\s+|\sand gazed\s+|\.\s*")
    df[col_name] = df[col_name].apply(lambda x: [i.lower() for i in x if i])
    
    df_tmp = pd.DataFrame(df[col_name].to_list(), columns=['src_type', 'dst_type'])
    df = pd.concat([df, df_tmp], axis=1)
    df = df.drop(col_name, axis=1)
    
    return df


def _talking_str2list(df, col_name="talking_description", drop_col_name="talking_id"):
    df_talking = df[col_name]
    assert_unique_item_df = len(set(df_talking))
    
    df_talking = df_talking.str.findall("\d")
    df_talking = df_talking.apply(lambda x: [int(i) for i in x])

    df[col_name] = df_talking

    assert assert_unique_item_df == len(set(df[col_name].apply(lambda x: str(x)+"-")))

    df = df.drop(columns=[drop_col_name])

    return df


def _position_str2list(df, col_name="position_description"):
    df[col_name] = df[col_name].str.split("Gazing sitting\s+|\sbeing gazed.\s*")
    df[col_name] = df[col_name].apply(lambda x: [i.lower() for i in x if i])
    
    df_tmp = pd.DataFrame(df[col_name].to_list(), columns=['position_type'])
    df = pd.concat([df, df_tmp], axis=1)
    df = df.drop(col_name, axis=1)
    
    return df


def _talking_enc_t1(df, col_name='speakers'):

    def chk_exist(id, speakers):
        if id in speakers:
            return 1
        else:
            return 0

    def chk_others(id, speakers):
        if id in speakers:
            if len(speakers) > 1:
                return 1
            else:
                return 0
        if len(speakers) > 0:
            return 1
        else:
            return 0
        
    df['src_talking_status'] = df.apply(lambda x: chk_exist(x['src_id'], x[col_name]), axis=1)
    df['dst_talking_status'] = df.apply(lambda x: chk_exist(x['dst_id'], x[col_name]), axis=1)
    df['others_talking_status'] = df.apply(lambda x: chk_others(x['src_id'], x[col_name]), axis=1)

    # df = df.drop(col_name, axis=1)
    
    return df


def _rename_df(df):
    df = df.rename(columns={
        "id": "src_id",
        "gaze_id": "dst_id",
        "talking_description": "speakers",
    })
    return df