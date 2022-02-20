import os
inpath = "C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract\\OMNI\\OLD\\"
outpath = "C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract\\OMNI\\NEW\\"
files = os.listdir(inpath)
for file in files:
    input_file = inpath+file
    output_file = outpath+file
    infile = open(input_file, 'r')
    outfile = open(output_file, 'w')
    start_tag_found = False
    end_tag_found = False
    first_half = ''
    second_half = ''
    for line in infile:
        if end_tag_found:
            outfile.write(line)
        else:
            if start_tag_found:
                if line.find("</notifylist>") == -1:
                    continue
                else:
                    end_tag_found = True
                    second_half = line.split("</notifylist>")[1]
                    #full_line = first_half+second_half
                    # outfile.write(full_line)
                    outfile.write(second_half)
            else:
                if line.find("<notifylist>") == -1:
                    outfile.write(line)
                else:
                    start_tag_found = True
                    first_half = line.split("<notifylist>")[0]
                    outfile.write(first_half)
                    if line.find("</notifylist>") == -1:
                        continue
                    else:
                        end_tag_found = True
                        second_half = line.split("</notifylist>")[1]
                        #full_line = first_half + ' ' + second_half
                        # outfile.write(full_line)
                        outfile.write(second_half)
    outfile.close()
    infile.close()
