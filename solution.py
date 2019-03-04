import sys

def solution(orientations, tags):

    slides = []
    v_slides = {}

    for i in range(len(orientations)):
        # Get vertical photos together; based on most common tags
        if orientations[i] == 'V':
            i_tags = set(tags[i])
            j_temp = i
            all_tags = 0
            for j in range(i+1, len(orientations)):
                if orientations[j] == 'V':
                    j_tags = set(tags[j])
                    curr_all_tags = len(i_tags | j_tags)
                    if curr_all_tags > all_tags:
                        j_temp = j
                        all_tags = curr_all_tags
                    if curr_all_tags == len(i_tags) + len(j_tags):
                        break
            win_jtgs = set(tags[j_temp])
            tags[i] = list(i_tags | win_jtgs)
            orientations[j_temp] = None
            v_slides[i] = j_temp

    # filter out tracked vertical photos
    _orientations = [[i, v, len(tags[i])]
                     for (i, v) in enumerate(orientations) if v is not None]

    _orientations.sort(key=lambda x: x[2])

    for i in range(len(_orientations)):
        image_i = _orientations[i][0]
        if _orientations[i][1] != 'X':
            i_tags = set(tags[image_i])
            score = 0
            j_temp = i
            for j in range(i+1, len(_orientations)):
                image_j = _orientations[j][0]
                if _orientations[j][1] != 'X':
                    j_tags = set(tags[image_j])
                    comm_tags = len(i_tags & j_tags)
                    if comm_tags == 0:
                        continue
                    if comm_tags == len(i_tags) or comm_tags == len(j_tags):
                        break
                    curr_min = min(comm_tags, len(
                        i_tags - j_tags), len(j_tags - i_tags))
                    if curr_min > score:
                        j_temp = j
                        score = curr_min
            slides.append(image_i)
            if j_temp != i:
                _orientations[j_temp][1] = 'X' #Flag current photo to not be comapred again
                slides.append(_orientations[j_temp][0])

    print(len(slides))
    for _, value in enumerate(slides):
        if value in v_slides:
            print(value, v_slides[value])
        else:
            print(value)


def main():
    if len(sys.argv) < 2:
        print('Missing dataset file name')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    photos_length, *photos = lines
    orientations = []
    tags = []

    for _, value in enumerate(photos):
        ori, _, *tgs = value.split(' ')
        orientations.append(ori)
        tags.append(tgs)

    solution(orientations, tags)

if __name__ == "__main__":
    main()
