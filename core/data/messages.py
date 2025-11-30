from textwrap import dedent

messages = {
    'start': {
        '_welcome_text': dedent("""
            👋 Привет, <b>{mention}</b>!
            Я — твой бот. Доступные команды: /help, пинг.
            Вот что я знаю о тебе:
            <blockquote>user_id: {user_id}
            full_name: {full_name}
            username: {username}</blockquote>
            
            Formats: <b>bold</b>, <i>italic</i>, <u>underline</u>, <s>strikethrough</s>, <code>monospace</code>, <tg-spoiler>tg-spoiler</tg-spoiler>
            <pre>pre-formatted</pre><blockquote extendable>blockquote extend</blockquote>
        """),
    },
}