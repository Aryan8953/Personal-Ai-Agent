from ddgs import DDGS


def search_web(query, max_results=5):

    query = str(query).strip()

    if not query:
        return "Search query is empty."

    try:

        results = DDGS().text(
            query,
            max_results=int(max_results)
        )

        if not results:
            return "No search results found."

        formatted = []

        for result in results:

            title = result.get(
                "title",
                "Untitled"
            )

            body = result.get(
                "body",
                ""
            )

            url = result.get(
                "href",
                ""
            )

            formatted.append(
                f"Title: {title}\n"
                f"Summary: {body}\n"
                f"URL: {url}"
            )

        return "\n\n".join(formatted)

    except Exception as error:

        return f"Web search failed: {error}"