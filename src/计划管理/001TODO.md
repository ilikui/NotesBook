> 计划管理


![](../Images/20230514/2023051401.png)
---

## 阶段学习任务安排




<!DOCTYPE html>
<html lang="en">

  <body>
    <div  class="mermaid">
        gantt
            dateFormat  YYYY-MM-DD
            title       2023年度学习计划
            excludes    weekends
            %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)

            section A section
            Completed task            :done,    des1, 2014-01-06,2014-01-08
            Active task               :active,  des2, 2014-01-09, 3d
            Future task               :         des3, after des2, 5d
            Future task2              :         des4, after des3, 5d

            section Critical tasks
            Completed task in the critical line :crit, done, 2014-01-06,24h
            Implement parser and jison          :crit, done, after des1, 2d
            Create tests for parser             :crit, active, 3d
            Future task in critical line        :crit, 5d
            Create tests for renderer           :2d
            Add to mermaid                      :1d
            Functionality added                 :milestone, 2014-01-25, 0d

            section Documentation
            Describe gantt syntax               :active, a1, after des1, 3d
            Add gantt diagram to demo page      :after a1  , 20h
            Add another diagram to demo page    :doc1, after a1  , 48h

            section Last section
            Describe gantt syntax               :after doc1, 3d
            Add gantt diagram to demo page      :20h
            Add another diagram to demo page    :48h
   </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    </script>
  </body>
</html>
















