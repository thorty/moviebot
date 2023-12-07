from st_supabase_connection import SupabaseConnection
import streamlit as st


def insert_conversation( usermessage, botmessage):
    try:
        conn = st.connection("supabase",type=SupabaseConnection)
        usermessage = usermessage.replace("'","")
        botmessage = botmessage.replace("'","")
        #query= "INSERT INTO messages VALUES ('"+usermessage+"','"+botmessage+"');"
        conn.table("messages").insert([{"usermsg":usermessage, "botmsg": botmessage}]).execute()
    except:
        return None


def fetchdata():
    conn = st.connection("supabase",type=SupabaseConnection)
    #query= "SELECT * FROM messages;"
    rows = conn.query("*", table="messages", ttl="10m").execute()    
    return rows