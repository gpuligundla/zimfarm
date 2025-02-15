<!-- Filterable list of schedules with filtered-fire button -->

<template>
  <div class="container">
    <nav class="row">
      <div class="col-sm-12 col-md-6 col-lg">
        <input type="text" class="form-control" v-model="selectedName" @change="loadSchedules" placeholder="Name…" />
      </div>
      <div class="col-sm-12 col-md-6 col-lg">
        <multiselect v-model="selectedCategoriesOptions"
                     :options="categoriesOptions"
                     :multiple="true"
                     :clear-on-select="true"
                     :preserve-search="true"
                     :searchable="true"
                     :closeOnSelect="true"
                     placeholder="Categories"
                     label="name"
                     track-by="value"
                     @input="loadSchedules">

        </multiselect>
      </div>
      <div class="col-sm-12 col-md-6 col-lg">
        <multiselect v-model="selectedLanguagesOptions"
                     :options="languagesOptions"
                     :multiple="true"
                     :clear-on-select="true"
                     :preserve-search="true"
                     :searchable="true"
                     :closeOnSelect="true"
                     placeholder="Languages"
                     label="name"
                     track-by="value"
                     @input="loadSchedules">

        </multiselect>
      </div>
      <div class="col-sm-12 col-md-6 col-lg">
        <multiselect v-model="selectedTagsOptions"
                     :options="tagsOptions"
                     :multiple="true"
                     :clear-on-select="true"
                     :preserve-search="true"
                     :searchable="true"
                     :closeOnSelect="true"
                     placeholder="Tags"
                     label="name"
                     track-by="value"
                     @input="loadSchedules">

        </multiselect>
      </div>
    </nav>
    <table v-if="schedules.length" class="table table-responsive-md table-striped table-hover table-bordered">
      <caption>Showing max. <select v-model="selectedLimit" @change.prevent="limitChanged">
          <option v-for="limit in limits" :key="limit" :value="limit">{{ limit }}</option>
        </select> out of <strong>{{ total_results }} results</strong>
        <RequestSelectionButton :for_name="selectedName"
                                :for_categories="selectedCategories"
                                :for_languages="selectedLanguages"
                                :for_tags="selectedTags"
                                :count="meta.count" />
        <b-button size="sm"
                  variant="secondary"
                  style="float:right;"
                  @click.prevent="clearSelection"
                  class="mr-1">clear <font-awesome-icon icon="times-circle" size="sm"/>
        </b-button>
      </caption>
      <thead class="thead-dark">
        <tr><th>Name</th><th>Category</th><th>Language</th><th>Offliner</th>
            <th v-tooltip="'Requested?'"><font-awesome-icon icon="clock"/></th><th colspan="2">Last Task</th></tr>
      </thead>
      <tbody>
        <tr v-for="schedule in schedules" :key="schedule._id">
          <td>
            <router-link :to="{name: 'schedule-detail', params: {'schedule_name': schedule.name}}">
              {{ schedule.name }}
            </router-link>
          </td>
          <td>{{ schedule.category }}</td>
          <td>{{ schedule.language.name_en }}</td>
          <td>{{ schedule.config.task_name }}</td>
          <td><font-awesome-icon v-if="schedule.is_requested" icon="check"/></td>
          <td v-if="schedule.most_recent_task">
            <code :class="statusClass(schedule.most_recent_task.status)">{{ schedule.most_recent_task.status }}</code>
          </td>
          <td colspan="2" v-else>-</td>
          <td v-if="schedule.most_recent_task">
            <TaskLink :_id="schedule.most_recent_task._id" :updated_at="schedule.most_recent_task.updated_at" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script type="text/javascript">
  import Constants from '../constants.js'
  import Multiselect from 'vue-multiselect'

  import ZimfarmMixins from '../components/Mixins.js'
  import RequestSelectionButton from '../components/RequestSelectionButton.vue'
  import TaskLink from '../components/TaskLink.vue'

  const filters_map = {"category": "Categories", "lang": "Languages", "tag": "Tags"};

  export default {
    name: 'SchedulesList',
    mixins: [ZimfarmMixins],
    components: {Multiselect, RequestSelectionButton, TaskLink},
    data() {
      return {
        error: null,  // API originated error message
        meta: {}, // API query metadata (count, skip, limit)
        schedules: [],  // list of schedules returned by the API
        block_url_updates: false,
      };
    },
    computed: {
      selectedLanguagesOptions: {  // multiple-select value for selected languages to filter on (union)
        set(selectedLanguagesOptions) {
          this.$store.commit('SET_SELECTED_LANGUAGES_OPTIONS', selectedLanguagesOptions);
          this.update_url();
        },
        get() {
          return this.$store.state.selectedLanguagesOptions;
        }
      },
      selectedCategoriesOptions: {  // multiple-select value for selected languages to filter on (union)
        set(selectedCategoriesOptions) {
          this.$store.commit('SET_SELECTED_CATEGORIES_OPTIONS', selectedCategoriesOptions);
          this.update_url();
        },
        get() {
          return this.$store.state.selectedCategoriesOptions;
        }
      },
      selectedTagsOptions: {  // multiple-select value for selected tags to filter on (intersection)
        set(selectedTagsOptions) {
          this.$store.commit('SET_SELECTED_TAGS_OPTIONS', selectedTagsOptions);
          this.update_url();
        },
        get() {
          return this.$store.state.selectedTagsOptions;
        }
      },
      selectedName: {  // entered regexp to match schedule names on
        set(selectedName) {
          this.$store.commit('SET_SELECTED_NAME', selectedName.trim());
          this.update_url();
        },
        get() {
          return this.$store.state.selectedName;
        }
      },
      selection() { return this.schedules.map(function (schedule){ return schedule.name; }); },
      total_results() {
        return (this.meta && this.meta.count) ? this.meta.count : 0;
      },
      categoriesOptions() {
        let options = [];
        for (var i=0; i<this.categories.length; i++){
          options.push({name: this.categories[i], value: this.categories[i]});
        }
        return options;
      },
      selectedCategories() { return this.selectedCategoriesOptions.map((x) => x.value); },
      languagesOptions() {
        let options = [];
        for (var i=0; i<this.languages.length; i++){
          options.push({name: this.languages[i].name_en, value: this.languages[i].code});
        }
        return options;
      },
      selectedLanguages() { return this.selectedLanguagesOptions.map((x) => x.value); },
      tagsOptions() {
        let options = [];
        for (var i=0; i<this.tags.length; i++){
          options.push({name: this.tags[i], value: this.tags[i]});
        }
        return options;
      },
      selectedTags() { return this.selectedTagsOptions.map((x) => x.value); },
    },
    methods: {
      clearSelection() {
        this.selectedName = "";
        this.selectedCategoriesOptions = [];
        this.selectedLanguagesOptions = [];
        this.selectedTagsOptions = [];
        this.loadSchedules();
      },
      limitChanged() {
        this.saveLimitPreference(this.selectedLimit);
        this.loadSchedules();
      },
      update_url(){
        if (this.block_url_updates || Constants.is_ios_firefox)
          return;

        let parent = this;
        // create query obj from selected fields
        let query = {};
        ["category", "lang", "tag"].forEach(function (paramName) {
          let filterLabel = filters_map[paramName];
          let selectedValues =  "selected" + filterLabel;
          // reproduce query-string behavior for single value
          if (parent[selectedValues].length == 1)
            query[paramName] = parent[selectedValues].first();
          else if (parent[selectedValues].length > 1)
            query[paramName] = parent[selectedValues];
        });
        if (this.selectedName.length > 0 )
          query["name"] = this.selectedName;

        // only update URL if filter selection is different
        if (!Object.isEqual(this.$route.query, query)) {
          this.$router.replace({name: "schedules-list", query: query});
        }
      },
      loadSchedules() {  // load filtered schedules from API
        let parent = this;
        this.toggleLoader("fetching recipes…");
        this.block_url_updates = true;

        // extracting filters info from URL query (for multiple-values)
        ["category", "lang", "tag"].forEach(function (filterName) {
          let filterLabel = filters_map[filterName];
          let selectedFilterOption =  "selected" + filterLabel + "Options";
          // only care about set filters
          let filterValue = parent.$route.query[filterName] || "";
          if (filterValue) {
            // update UI if there's no input there (loading URL)
            if (parent[selectedFilterOption].length == 0) {
              // multiple value fields appear as regular string if there's a single value
              if (typeof filterValue === "string") {
                parent[selectedFilterOption] = [{name: filterValue, value: filterValue}];
              } else {
                for(var i=0; i<parent.$route.query[filterName].length; i++) {
                  parent[selectedFilterOption] = {name: filterValue, value: filterValue[i]};
                }
              }
            }
          }
        });

        // extract name from URL query
        if (this.$route.query.name) {
          // update UI
          if (this.selectedName.trim().length == 0) {
              this.selectedName = this.$route.query.name;
          }
        }

        // create request params based on UI selection so its consistent
        let params = {limit: parent.selectedLimit};
        if (this.selectedLanguages.filter(item => item.length).length) {
          params.lang = this.selectedLanguages;
        }
        if (this.selectedTags.filter(item => item.length).length) {
          params.tag = this.selectedTags;
        }
        if (this.selectedCategories.filter(item => item.length).length) {
          params.category = this.selectedCategories;
        }
        if (this.selectedName.length) {
          params.name = this.selectedName;
        }

        parent.error = null;
        parent.queryAPI('get', '/schedules/', {params: params})
          .then(function (response) {
                parent.schedules = [];
                parent.meta = response.data.meta;
                parent.schedules = response.data.items;
          })
          .catch(function (error) {
            parent.schedules = [];
            parent.standardErrorHandling(error);
          })
          .then(function () {
            parent.toggleLoader(false);
            parent.block_url_updates = false;
            // trigger update_url so it matches selection in case url was empty
            parent.update_url();
          });
      },
    },
    beforeMount() {
      this.loadSchedules();
    },
  }
</script>

<style type="text/css" scoped>
  .container table.table {
    margin-top: .5rem;
  }
  .container input[type=text] {
    height: 100%;
  }
  .col-sm-12 {
    margin-bottom: .25rem;
  }
</style>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
