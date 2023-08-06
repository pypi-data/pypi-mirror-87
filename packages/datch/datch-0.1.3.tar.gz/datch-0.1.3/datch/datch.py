import os
import pandas as pd
import datch.errors


def check(input_file=None, sheet_name=None, output_file=None):
    
    # check path for inputfile and outputfile
    if input_file[0] != os.path.sep:
        input_file = os.path.sep + input_file

    if output_file is None:
        file_path, file_name_full = os.path.split(input_file)
        file_name, file_extension = os.path.splitext(file_name_full)
        output_file = file_path + os.path.sep + file_name + '_datched' + file_extension
    elif output_file[0] != os.path.sep:
        output_file = os.path.sep + ououtput_filetput

    # read the data
    sheets_dict = pd.read_excel(os.getcwd()+input_file, sheet_name=sheet_name)

    # create new excel file
    writer = pd.ExcelWriter(os.getcwd()+output_file, engine='xlsxwriter', options={'remove_timezone': True}, datetime_format='mmm d yyyy hh:mm:ss', date_format='mmmm dd yyyy')
    workbook  = writer.book

    # set defaults
    marked_cell_format = workbook.add_format({'bg_color': '#ffcccc'})

    if isinstance(sheets_dict, pd.DataFrame):
        sheets_dict = {sheet_name: df}
    
    for name, df in sheets_dict.items():
    
        # write the data to a new file and select the worksheet
        df.to_excel(writer, sheet_name=name, index=False)
        worksheet = writer.sheets[name]

        for col, col_name in enumerate(df.columns):

            # comment with general info in title
            #worksheet.write_comment(0, col, comment(general_info(df[col_name])), {'x_scale': 1.2, 'y_scale': 0.8})

            # get errors
            error_list = datch.errors.any(df[col_name]).errors

            nan_errors = datch.errors.nan(df[col_name])
            caps_errors = datch.errors.caps(df[col_name])
            whitespace_errors = datch.errors.whitespace(df[col_name])
            dtype_errors = datch.errors.dtype(df[col_name])
            

            for idx, val in df[col_name][error_list].items():
                worksheet.set_row(idx+1, None, marked_cell_format)
                    
                # add comment    
                if idx in df[col_name][nan_errors.errors].index.values:
                    worksheet.write_comment(idx + 1, col, f'Empty field. Expected a {dtype_errors.suggestions[idx]} value.')

                elif idx in df[col_name][caps_errors.errors].index.values:
                    worksheet.write_comment(idx + 1, col, f'Unexpected CAPS usage. Suggested value: \'{str(caps_errors.suggestions[idx])}\'')

                elif idx in df[col_name][whitespace_errors.errors].index.values:
                    worksheet.write_comment(idx + 1, col, f'Unexpected white space. Suggested value: \'{str(whitespace_errors.suggestions[idx])}\'')

                elif idx in df[col_name][dtype_errors.errors].index.values:
                    worksheet.write_comment(idx + 1, col, f'Unexpected {str(dtype_errors.values[idx])} value. Expected a {dtype_errors.suggestions[idx]} value.')
    writer.save()
    print(f"DatCh is done! The output file is saved as {output_file}")

def main(args):
    input_file = args.input_file
    output_file = args.output_file
    sheet_name = args.sheet_name
    
    # check path for inputfile and outputfile
    if input_file[0] != os.path.sep:
        input_file = os.path.sep + input_file

    if output_file is None:
        file_path, file_name_full = os.path.split(input_file)
        file_name, file_extension = os.path.splitext(file_name_full)
        output_file = file_path + os.path.sep + file_name + '_datched' + file_extension
    elif output_file[0] != os.path.sep:
        output_file = os.path.sep + output_file

    datch(input_file=input_file, sheet_name=sheet_name, output_file=output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help=f"set the relative path and the name of the input file; e.g. {os.path.sep}data{os.path.sep}data.xlsx")
    parser.add_argument("-o", "--output_file", help=f"set the relative path and the name of the output file; e.g. {os.path.sep}ptoutput{os.path.sep}output.xlsx", default="output.xlsx")
    parser.add_argument("-s", "--sheet_name", help=f"set the sheet name; e.g. \"data\" (default value = None, checks all sheets)", default=None)
    args = parser.parse_args()
    main(args)