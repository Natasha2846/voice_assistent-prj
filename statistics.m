clear; clc; clear
filename = 'statistics.csv';
Format  = 'dd.mm.yy';
data = fopen(filename);
A = textscan(data,'%s','Delimiter','\n');
A = A{1};
C = [];
Date = cell(length(A), 1); Time = cell(length(A), 1); Task = cell(length(A), 1);
for i=1:length(A)
    C = textscan(A{i},'%s','Delimiter',',');
    Task{i,1} = C{1}{2};
    Time{i,1} = C{1}{3};
    Date{i,1} = C{1}{1};
end
fclose(data);

uTask = unique(Task);
uDate = convertCharsToStrings(unique(Date));
A = zeros(length(unique(Date)),length(uTask));

for j=1:length(Date)
    for k=1:length(uDate)
        uDateChars = uDate(k);
        DateChars = convertCharsToStrings(Date(j));
        if uDateChars == DateChars
            for i=1:length(uTask)
                if convertCharsToStrings(Task{j,1}) == convertCharsToStrings(uTask{i})
                    A(k,i) = str2double(Time{j});
                end
            end
        end
    end
end
Bar = bar(A,'stacked');

% A loop that does num2str conversion only if value is >0
for i=1:size(A,1)
    for j=1:size(A,2)
        if A(i,j)>0
        labels_stacked = num2str(A(i,j),'%.1f m');
        hText = text(i, sum(A(i,1:j),2), labels_stacked);
        set(hText, 'VerticalAlignment','top', 'HorizontalAlignment', 'center','FontSize',10, 'Color','w');
        end
    end
end

set(gca,'xticklabel',uDate, 'FontSiz', 8, 'XTickLabelRotation', 45);
grid on
legend(uTask,'Location','northwest')