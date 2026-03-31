mymovielst = [
    {"title": "Attack on Titan: Chronicle", "genres": ["action", "adventure", "drama"], "mood": "intense", "year": 2020, "popularity": 89, "story": "After giant Titans break through humanity's walls, Eren and his friends fight for survival and uncover dangerous truths about their world."},
    {"title": "Grave of the Fireflies", "genres": ["war", "drama", "animation"], "mood": "sad", "year": 1988, "popularity": 90, "story": "Two orphaned siblings struggle to survive in Japan during the final months of World War II after losing their home and family."},
    {"title": "Interstllar", "genres": ["sci-fi", "adventure", "drama"], "mood": "thoughtful", "year": 2014, "popularity": 97, "story": "A former pilot joins a space mission through a wormhole to find a new home for humanity as Earth slowly becomes unlivable."},
    {"title": "Oppenhimer", "genres": ["biography", "drama", "history"], "mood": "serious", "year": 2023, "popularity": 96, "story": "The film follows J. Robert Oppenheimer as he leads the Manhattan Project and faces the moral weight of helping create the atomic bomb."},
    {"title": "A Beautifl Mind", "genres": ["biography", "drama"], "mood": "inspiring", "year": 2001, "popularity": 88, "story": "Brilliant mathematician John Nash battles schizophrenia while trying to protect his work, his marriage, and his sense of reality."},
    {"title": "A Silent Voice", "genres": ["animation", "drama"], "mood": "emotional", "year": 2016, "popularity": 87, "story": "A former bully tries to make amends with a deaf girl he once hurt, leading both of them toward healing, forgiveness, and self-acceptance."},
]
def sinput(text):
    return [part.strip().lower() for part in text.split(",") if part.strip()]
def keywordl(text):
    fword, cword = [], ""
    for letter in text.lower():
        if letter.isalnum():
            cword += letter
        else:
            if len(cword) > 3:
                fword.append(cword)
            cword = ""
    if len(cword) > 3:
        fword.append(cword)
    return fword
def ppmovie(mlist):
    rmovie = []
    for movie in mlist:
        new_movie = movie.copy()
        new_movie["keywords"] = keywordl(movie["story"])
        rmovie.append(new_movie)
    return rmovie
def taste(mlist, favorite, cmovie, rating):
    profile = {}
    for genre in favorite:
        profile[genre] = profile.get(genre, 0) + 3
    if cmovie:
        profile[cmovie] = profile.get(cmovie, 0) + 2
    for movie in mlist:
        stars = rating.get(movie["title"], 0)
        if stars >= 4:
            for genre in movie["genres"]:
                profile[genre] = profile.get(genre, 0) + stars
            for word in movie["keywords"][:4]:
                profile[word] = profile.get(word, 0) + 1
        elif stars and stars <= 2:
            for genre in movie["genres"]:
                profile[genre] = profile.get(genre, 0) - 2
    return profile
def score(movie, profile):
    tscore = movie["popularity"] / 20
    for genre in movie["genres"]:
        tscore += profile.get(genre, 0)
    tscore += profile.get(movie["mood"], 0)
    for word in movie["keywords"][:4]:
        tscore += profile.get(word, 0) * 0.5
    return round(tscore, 2)
def greason(movie, favorite, cmovie):
    genre = [genre.title() for genre in movie["genres"] if genre in favorite]
    if genre:
        return "Matches your favorite genres: " + ", ".join(genre)
    if movie["mood"] == cmovie:
        return "Fits your current mood: " + movie["mood"].title()
    return "Looks close to the movies you rated highly"
def main():
    movies = ppmovie(mymovielst)
    print("=" * 60)
    print("SIMPLE AI MOVIE RECOMMENDER")
    print("=" * 60)
    username = input("Enter your name: ").strip() or "Movie Lover"
    agenres = sorted({genre for movie in movies for genre in movie["genres"]})
    print("\nAvailable genres:", ", ".join(genre.title() for genre in agenres))
    favorite = sinput(input("Enter 2 or 3 favorite genres: "))
    cmovie = input("Enter your current mood: ").strip().lower()
    print("\nRate a few movies from 1 to 5 so the system can learn your taste.")
    rating = {}
    for movie in movies[:4]:
        reply = input(f"{movie['title']}: ").strip()
        if reply.isdigit() and 1 <= int(reply) <= 5:
            rating[movie["title"]] = int(reply)
    profile = taste(movies, favorite, cmovie, rating)
    recommendations = []
    for movie in movies:
        if movie["title"] not in rating:
            recommendations.append((score(movie, profile), movie))
    recommendations.sort(key=lambda item: item[0], reverse=True)
    print(f"\nTop recommendations for {username}:\n")
    for count, (score, movie) in enumerate(recommendations[:3], start=1):
        print(f"{count}. {movie['title']} ({movie['year']}) - Score {score}")
        print("   " + greason(movie, favorite, cmovie))
        print("   " + movie["story"])
if __name__ == "__main__":
    main()