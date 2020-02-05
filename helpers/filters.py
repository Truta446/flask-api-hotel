def normalize_data(city=None, min_stars=0, max_stars=5, min_dayly=0, max_dayly=10000, limit=50, offset=0):
    if city:
        return {
            'city': city,
            'min_stars': min_stars,
            'max_stars': max_stars,
            'min_dayly': min_dayly,
            'max_dayly': max_dayly,
            'limit': limit,
            'offset': offset
        }

    return {
        'min_stars': min_stars,
        'max_stars': max_stars,
        'min_dayly': min_dayly,
        'max_dayly': max_dayly,
        'limit': limit,
        'offset': offset
    }


consult_with_city = "SELECT * FROM hotels \
    WHERE city = ? \
    AND stars BETWEEN ? AND  ? \
    AND dayly BETWEEN ? AND ? \
    LIMIT ? \
    OFFSET ?"

consult_without_city = "SELECT * FROM hotels \
    WHERE stars BETWEEN ? AND  ? \
    AND dayly BETWEEN ? AND ? \
    LIMIT ? \
    OFFSET ?"
