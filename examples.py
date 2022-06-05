def annotation():
    from annotated_text import annotated_text
    annotated_text("hello ", ('this', 'prop'), ' is quite neat')


def graphwiz():
    import streamlit as st
    st.graphviz_chart("""

    digraph L {

      node [shape=record fontname=Arial];

      a  [label="one\ltwo three\lfour five six seven\l"]
      b  [label="one\ntwo three\nfour five six seven"]
      c  [label="one\rtwo three\rfour five six seven\r"]

      a -> b -> c

    }
    """)


def timeline():
    from lib.timeline import Timeline
    Timeline.example()
