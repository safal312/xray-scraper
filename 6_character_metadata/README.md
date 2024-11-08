**Order of Execution**
- `extract_names.py`: This script gathers all the names from the remaining movies that have valid x-rays into one file.

- `get_valid_movies.ipynb`: This notebook gets the metadata for all the remaining valid movies that have at least one person in the movie.

- `imdb_matching.py`: This script runs the algorithm to find the correct imdb id of a movie based on the cast list. We search movies first based on the title and get top 5 results. We take the top 5 cast of each movie based on the order (generally, more influential characters are placed in the top 5 positions of the cast list in IMDb). Now, we check for intersection between the cast list from our x-ray data and the top 5 cast from the imdb listing. Among the 5 search results, we iteratively look for an imdb listing that has at least one person that intersects.

- `metadata_merge.ipynb`: This notebook merges current list of movies with valid xrays with metadata collected from `2_parse_links` to get all the necessary details of a movie. It removes unnecessary columns as well. We use the final file for validation purpose.

- `validation_helper/validate.py`: This script opens up two windows side-by-side - the left one searches in google a string of format `<title_of_movie> imdb movie <release_year>`. This gives back closely matched search results. On the right hand, we have the prime video page of the movie for reference. You can then use the information from Prime video to determine if a movie's a match. On the terminal, you'll be asked three questions: "Was this a match (0 or 1)?" whose value is 0 of course since we don't have any imdb ids to match, "Alternative IDs:" where we can enter the new imdb ID manually, and "Any notes?" to note any observations. After filling these questions, an entry is made the output file with the added details from the questions.

- `validation_helper/utils/`:
    - `FileHandler.py`: Helper class to read the input file, save the output file.
    - `FirefoxDriver.py`: Helper class to start two windows for validation.
    - `UserInput.py`: Helper class to handle the QA to collect details about the validation process. Asks questions in the terminal.

- `validation_helper/merge_validated.ipynb`: Fills `metadata_for_validation.csv` file with the validated imdb IDs that were initially missing.

- `support_crew/get_crew.py`: Uses Cinemagoer library to extract data of all the support crew for the movies in our dataset.

- `validate_metadata_xray/check_xray_sanity.ipynb`: Check for cases where x-ray file is duplicated for different movies. Manually inspect such issues and remove the actual duplicates.

- `validate_metadata_xray/check_title_mismatched.ipynb`: Check cases where the metadata file (Playback Resources) might have been duplicated.

- `validate_metadata_xray/fix_metadata_mismatch.ipynb`: We fix the cases where the Playback Resources are duplicates/mismatches and refill proper metadata using the imdb ID which is correct.

**Files**
- `extract_names.py`:
    - `Inputs`:
        - `../data/4_parsed_xrays/{target_dir}/{target_dir}_sub_movies_with_xrays.csv`: We make use of the metadata of movies with valid xrays, generated from `4_parse_xrays` module. Using the file names from the `file` column, we open each movie's respective `people.csv` file and save it into a common dataframe.

    - `Outputs`:
        - `../data/6_character_metadata/all_people_with_duplicates.csv`: The script generates a file which has all the cast from every movie in one file.
        - `../data/6_character_metadata/all_people.csv`: This file is similar, but duplicates based on each person's unique imdb name ID have been removed to get a list of all unique people in our dataset.

- `get_valid_movies.ipynb`:
    - `Inputs`:
        - `../data/4_parsed_xrays/{dir}_sub_movies_with_xrays.csv`: We use the metadata of all the movies with valid xrays. We combine the metadata of all batches together and fill in any missing values. For example, `title` was missing for some entries. Therefore, we used the metadata file `../data/2_metadata/{dir}/clean_meta_en_prime.csv` to fill such cases.

    - `Outputs`:
        - `../data/6_character_metadata/movies_with_cast_manual.csv`: This is the dataset with the metadata of all movies with valid xrays in our dataset.

- `imdb_matching.py`:
    - `Inputs`:
        - `../data/6_character_metadata/all_people_with_duplicates.csv`: List of people in each movie to compare imdb cast list with
        - `../data/6_character_metadata/movies_with_cast_manual.csv`: All movies with valid xray data
    
    - `Outputs`:
        - `../data/6_character_metadata/movies_with_ids.csv`: Output file is same as `movies_with_cast_manual.csv` with couple of new columns:
            - `imdb_id`: Movie ID matched by algorithm.
            - `match_error`: No. of unmatched people between the movie's cast list and our xray data. 
            - `cast_num`: Total IMDb cast for movie matched (Max 5 because of top 5 cast limit).

- `metadata_merge.ipynb`:
    - `Inputs`:
        - `../data/6_character_metadata/movies_with_ids.csv`: Metadata of movies with valid xrays.
        - `../data/2_metadata/{target_dir}/clean_meta_en_prime.csv`: Metadata files of different batches parsed from `2_parse_links` module.
    
    - `Outputs`:
        - `../data/6_character_metadata/metadata_for_validation.csv`: Combined metadata file of all the valid movies. This file is necessary for the validation step.

- `validation_helper/validate.py`:
    - `Inputs`:
        - `../../data/6_character_metadata/metadata_for_validation.csv`: This file is generated by `metadata_merge.ipynb` for this manual data collection and validation.
    
    - `Outputs`:
        - `../../data/6_character_metadata/validated_metadata.csv`: A new line is added to this file every time we validate a movie. This file has all the movies for which imdb IDs were missing.

- `validation_helper/merge_validated.ipynb`:
    - `Inputs`:
        - `../../data/6_character_metadata/metadata_for_validation.csv`: Original metadata of valid movies for validation.
        - `../../data/6_character_metadata/validated_metadata.csv`: Final metadata file of movies with missing imdb IDs.
    
    - `Outputs`:
        - `../../data/6_character_metadata/final_validated_metadata.csv`: Metadata file with the missing imdb IDs filled in.

- `support_crew/get_crew.py`:
    - `Inputs`:
        - `../../data/6_character_metadata/final_validated_metadata.csv`: Metadata of all movies in our dataset.
    - `Outputs`:
        - `../../data/6_character_metadata/movies_support_crew_with_manual.csv`: File with data of all support crew. It has the following columns:
            - `imdb_id`: IMDb id of movie
            - `file`: File identifier of movie in our dataset
            - `role`: Role of person in our movie
            - `name_id`: Name ID of person in IMDb
            - `name`: Name of person in IMDb
            - `long_canonical_name`: Name in canonical format
            - `headshot`: Link to headshot of person

- `validate_metadata_xray/check_xray_sanity.ipynb`:
    - `Inputs`:
        - `../../data/6_character_metadata/final_validated_metadata.csv`: This is the metadata file with the missing imdb ids filled in.
        - `../../data/6_character_metadata/all_people_with_duplicates.csv`: We inspect the cast extracted from x-ray data for different movies from this file. We check for duplicates based on cast information.
        - `../../data/6_character_metadata/metadata_for_validation.csv`: This file is generated after doing the imdb matching. Among the entries, the ones that weren't matched could likely be because the cast information from x-ray didn't match the corresponding imdb entry because it was incorrect. We can use this file to identify such cases and remove them.
    - `Outputs`:
        - `../../data/6_character_metadata/filtered_final_validated_metadata.csv`: This file is the generated after removing the potential duplicates. We encountered some entries that were comedy stand-ups which showed up because it usually has one person as the cast and they have multiple shows on the platform. We remove such cases as well to have a clean file with all movies.

- `validate_metadata_xray/check_title_mismatched.ipynb`:
    - `Inputs`:
        - `../../data/6_character_metadata/final_validated_metadata.csv`: This file can be used to detect the duplicates, but you can also use it with `filtered_final_validated_metadata.csv` in other runs.
    - `Outputs`:
        - `./check_title_mismatch.csv`: This file is created by identifying potential duplicates based on the discrepancy in the title of the movie and the unique file identifier. The approach is described in the notebook. We manually check if the movies are actually duplicates and create a copy of this file manually with a subset of the entries and save it as `./manually_checked_title_mismatch.csv`.

- `validate_metadata_xray/fix_metadata_mismatch.ipynb`:
    - `Inputs`:
        - `./manually_checked_title_mismatch.csv`: This is the manually created file with actual metadata mismatches.
        - `../../data/6_character_metadata/filtered_final_validated_metadata.csv`: This is the metadata file filtered after removing entries with duplicate x-rays. This file also has imdb ID which can be used to extract the real title and synopsis from IMDb.
    - `Outputs`:
        - `../../data/6_character_metadata/all_metadata_finalized.csv`: This is the final metadata file which is generated with correct metadata.