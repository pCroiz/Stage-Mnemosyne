for j = 1:5
    utterance_1 = struct("digit_0","")

    for i = 1:10
        utterance_1 = setfield(utterance_1,"digit_"+(i-1),Input(j,i,1).cochleogram)
    end

    utterance_2 = struct("digit_0","")

    for i = 1:10
        utterance_2 = setfield(utterance_2,"digit_"+(i-1),Input(j,i,2).cochleogram)
    end

    utterance_3 = struct("digit_0","")

    for i = 1:10
        utterance_3 = setfield(utterance_3,"digit_"+(i-1),Input(j,i,3).cochleogram)
    end

    utterance_4 = struct("digit_0","")

    for i = 1:10
        utterance_4 = setfield(utterance_4,"digit_"+(i-1),Input(j,i,4).cochleogram)
    end

    utterance_5 = struct("digit_0","")

    for i = 1:10
        utterance_5 = setfield(utterance_5,"digit_"+(i-1),Input(j,i,5).cochleogram)
    end

    utterance_6 = struct("digit_0","")

    for i = 1:10
        utterance_6 = setfield(utterance_6,"digit_"+(i-1),Input(j,i,6).cochleogram)
    end

    utterance_7 = struct("digit_0","")

    for i = 1:10
        utterance_7 = setfield(utterance_7,"digit_"+(i-1),Input(j,i,7).cochleogram)
    end

    utterance_8 = struct("digit_0","")

    for i = 1:10
        utterance_8 = setfield(utterance_8,"digit_"+(i-1),Input(j,i,8).cochleogram)
    end

    utterance_9 = struct("digit_0","")

    for i = 1:10
        utterance_9 = setfield(utterance_9,"digit_"+(i-1),Input(j,i,9).cochleogram)
    end

    utterance_10 = struct("digit_0","")

    for i = 1:10
        utterance_10 = setfield(utterance_10,"digit_"+(i-1),Input(j,i,10).cochleogram)
    end

    save("subject_"+j+".mat","utterance_1","utterance_2","utterance_3","utterance_4","utterance_5","utterance_6","utterance_7","utterance_8","utterance_9","utterance_10",'-v7.3')
end