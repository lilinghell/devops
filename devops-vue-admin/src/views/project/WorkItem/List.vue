<template>
  <div class="board">
    <q-toolbar class="bg-white text-blue-grey-9">
      <div class="row q-gutter-x-lg">
        <Field contracted>
          <template v-slot:label>
            <span class="text-blue-grey-9 text-weight-medium">模块</span>
          </template>
          <q-select
            dense
            options-dense
            use-input
            hide-dropdown-icon
            outlined
            v-model="filter.module"
            :options="modules"
            @filter="moduleFilter"
            class="toolbar-search"
            popup-content-class="q-mt-xs q-py-sm"
          >
            <template v-slot:no-option>
              <q-item dense class="option">
                <q-item-section side>
                  <q-icon name="warning" size="16px" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    没有可用数据
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:append>
              <q-btn
                size="sm"
                flat
                dense
                round
                icon="clear"
                v-if="filter.module"
                @click.prevent.stop="filter.module = ''"
              />
            </template>
            <template v-slot:option="scope">
              <q-item
                dense
                v-bind="scope.itemProps"
                v-on="scope.itemEvents"
                class="option"
                :class="scope.selected ? 'selected' : ''"
              >
                <q-item-section>
                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                </q-item-section>
                <q-item-section side v-if="scope.selected">
                  <q-item-label>
                    <q-icon name="done" class="text-primary text-weight-bold" />
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </Field>
        <Field contracted>
          <template v-slot:label>
            <span class="text-blue-grey-9 text-weight-medium">处理人</span>
          </template>
          <q-select
            dense
            options-dense
            use-input
            hide-dropdown-icon
            outlined
            multiple
            use-chips
            v-model="filter.assignee_users"
            :options="assignee_users"
            @filter="assignee_usersFilter"
            class="toolbar-search"
            style="max-width: initial"
            popup-content-class="q-mt-xs q-py-sm"
          >
            <template v-slot:no-option>
              <q-item dense class="option">
                <q-item-section side>
                  <q-icon name="warning" size="16px" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    没有可用数据
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:append>
              <q-btn
                size="sm"
                flat
                dense
                round
                icon="clear"
                v-if="filter.assignee_users.length > 0"
                @click.prevent.stop="filter.assignee_users = []"
              />
            </template>
            <template v-slot:option="scope">
              <q-item
                v-close-popup
                dense
                v-bind="scope.itemProps"
                v-on="scope.itemEvents"
                class="option"
                :class="scope.selected ? 'selected' : ''"
              >
                <q-item-section>
                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                </q-item-section>
                <q-item-section side v-if="scope.selected">
                  <q-item-label>
                    <q-icon name="done" class="text-primary text-weight-bold" />
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </Field>
      </div>
      <q-space />
      <div class="row q-gutter-x-sm">
        <q-btn
          unelevated
          class="toolbar-control btn-setting"
          icon="mdi-set mdi-tune"
        >
          <q-popup-proxy
            anchor="bottom right"
            self="top right"
            :offset="[103, 4]"
          >
            <q-splitter :value="60" disable class="popup-setting">
              <template v-slot:before>
                <q-card>
                  <q-card-section>
                    <TagSelect
                      label="标签"
                      size="sm"
                      v-model="filter.labels"
                      :options="labels"
                      label-width="60px"
                    >
                      <template v-slot:option="scope">
                        <q-btn
                          :key="scope.opt.value"
                          class="q-px-sm tag-label"
                          :color="scope.selected ? 'primary' : 'blue-grey-3'"
                          size="sm"
                          unelevated
                          v-on="scope.itemEvents"
                        >
                          <q-icon
                            name="mdi-set mdi-tag"
                            :style="
                              `color: ${
                                scope.selected ? 'white' : scope.opt.color
                              }`
                            "
                            class="on-left"
                          />
                          <span>{{ scope.opt.title }}</span>
                        </q-btn>
                      </template>
                    </TagSelect>
                  </q-card-section>
                </q-card>
              </template>
              <template v-slot:after>
                <q-list class="q-py-sm">
                  <q-item dense tag="label" v-ripple>
                    <q-item-section>
                      <q-item-label caption>只看我的</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-toggle dense v-model="filter.isMine" />
                    </q-item-section>
                  </q-item>
                  <q-item dense>
                    <q-item-section side>
                      <q-item-section>
                        <q-item-label caption>完成进度</q-item-label>
                      </q-item-section>
                    </q-item-section>
                    <q-item-section>
                      <q-slider v-model="filter.progress" label />
                    </q-item-section>
                  </q-item>
                </q-list>
              </template>
              <a class="btn-reset" @click="resetFilter">重置</a>
            </q-splitter>
          </q-popup-proxy>
        </q-btn>
        <q-btn
          unelevated
          dense
          label="看板视图"
          icon="mdi-set mdi-view-dashboard"
          class="toolbar-control q-mr-xs"
          v-if="view === 'table'"
          @click="view = 'kanban'"
        />
        <q-btn
          unelevated
          dense
          label="列表视图"
          icon="mdi-set mdi-table-large"
          class="toolbar-control q-mr-xs"
          v-if="view === 'kanban'"
          @click="view = 'table'"
        />
      </div>
    </q-toolbar>
    <div class="column-wrapper q-col-gutter-x-md" v-if="view === 'kanban'">
      <q-list
        class="board-column"
        v-for="(each, index) in categories"
        :key="each.value"
      >
        <div class="container">
          <div class="header row items-center">
            {{ each.label }}({{ each.workItems.length }})
          </div>
          <div class="body scroll scrollbar-hidden">
            <Loading :visible="globalLoading">
              <Draggable
                ref="draggable"
                :key="each.value"
                v-model="each.workItems"
                :animation="200"
                group="workItems"
                class="q-gutter-y-sm"
                style="min-height: 10px;"
                @change="evt => handleChange(evt, each)"
              >
                <q-item
                  v-ripple
                  clickable
                  @click="handleUpdateOpened(workItem)"
                  v-for="workItem in each.workItems"
                  :key="workItem.id"
                  class="item"
                  :class="priorityClass[workItem.priority]"
                >
                  <div class="text-weight-bold">{{ workItem.title }}</div>
                  <div class="text-subtitle2">{{ workItem.id }}</div>
                  <div class="text-subtitle2">{{ workItem.feature.title }}</div>
                  <div class="row items-center">
                    <div class="col">
                      <q-badge
                        align="middle"
                        class="col bg-red-5"
                        v-if="Date.now() > Date.parse(workItem.end_date)"
                      >
                        <q-icon name="access_time" class="q-mr-xs" />{{
                          workItem.end_date | moment('MM月DD日')
                        }}
                        <q-tooltip
                          :offset="[0, 5]"
                          transition-show="fade"
                          transition-hide="fade"
                          anchor="bottom left"
                          self="top left"
                          >已过期</q-tooltip
                        >
                      </q-badge>
                    </div>
                    <div class="gutter-avatar">
                      <q-avatar
                        v-for="user in workItem.assignee_users.slice(0, 3)"
                        :key="user.id"
                        size="28px"
                      >
                        <q-img :src="user.avatar_url" />
                      </q-avatar>
                    </div>
                  </div>

                  <q-btn
                    flat
                    dense
                    rounded
                    size="12px"
                    icon="more_horiz"
                    color="blue-grey-9"
                    class="absolute-top-right q-ma-sm"
                    @click.prevent.stop
                  >
                    <q-menu
                      @before-show="handleUpdatePopupWorkItemOpened(workItem)"
                    >
                      <q-list separator class="workItem-popup">
                        <q-form
                          ref="workItemPopupForm"
                          @submit="handleUpdatePopupWorkItem"
                        >
                          <q-input
                            filled
                            square
                            v-model="$v.popupUpdateModel.title.$model"
                            type="text"
                            dense
                            :error="$v.popupUpdateModel.title.$error"
                            hide-bottom-space
                            ref="workItem-popup-title"
                          >
                            <template v-slot:prepend>
                              <span class="field">任务名称：</span>
                            </template>
                          </q-input>
                        </q-form>
                        <q-item>
                          <TagSelect
                            label="处理人"
                            label-width="60px"
                            size="sm"
                            v-model="workItem.assignee_users"
                            :options="users"
                            emit-opt
                            sort
                            expandable
                            max-height="56px"
                            @input="() => handleUpdatePopupWorkItem(workItem)"
                          >
                            <template v-slot:option="scope">
                              <q-chip
                                dense
                                v-on="scope.itemEvents"
                                :selected="scope.selected"
                                :key="scope.opt.value"
                                :color="scope.selected ? 'primary' : ''"
                                :text-color="scope.selected ? 'white' : ''"
                              >
                                <q-avatar>
                                  <img :src="scope.opt.avatar_url" />
                                </q-avatar>
                                {{ scope.opt.name }}
                              </q-chip>
                            </template>
                          </TagSelect>
                        </q-item>
                        <q-item>
                          <TagSelect
                            label="标签"
                            label-width="60px"
                            size="sm"
                            v-model="workItem.labels"
                            :options="labelOptions"
                            emit-opt
                            @input="() => handleUpdatePopupWorkItem(workItem)"
                          >
                            <template v-slot:option="scope">
                              <q-btn
                                :key="scope.opt.value"
                                class="q-px-sm tag-label"
                                :color="
                                  scope.selected ? 'primary' : 'blue-grey-3'
                                "
                                size="sm"
                                unelevated
                                v-on="scope.itemEvents"
                              >
                                <q-icon
                                  name="mdi-set mdi-tag"
                                  class="on-left"
                                  :style="
                                    `color: ${
                                      scope.selected ? 'white' : scope.opt.color
                                    }`
                                  "
                                />
                                <span>{{ scope.opt.title }}</span>
                              </q-btn>
                            </template>
                          </TagSelect>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </q-item>
                <q-form ref="addForm" @submit="handleAdd(each, index)">
                  <q-input
                    v-if="each.addOpened"
                    v-model="$v.addModel.title.$model"
                    dense
                    type="text"
                    autofocus
                    placeholder="请输入标题"
                    :rules="[() => !$v.addModel.title.$error || '请输入标题']"
                  >
                    <template v-slot:append>
                      <q-btn
                        flat
                        dense
                        round
                        size="12px"
                        icon="more_horiz"
                        color="blue-grey-9"
                      >
                        <q-menu>
                          <q-list dense>
                            <q-item clickable v-close-popup>
                              <q-item-section>处理人</q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup>
                              <q-item-section>标签</q-item-section>
                            </q-item>
                          </q-list>
                        </q-menu>
                      </q-btn>
                    </template>
                  </q-input>
                </q-form>
              </Draggable>
            </Loading>
          </div>
          <transition-group
            tag="div"
            class="footer"
            :duration="300"
            enter-active-class="animated slideInUp absolute"
            leave-active-class="animated slideOutDown absolute"
          >
            <a
              key="open"
              v-show="!each.addOpened"
              @click="handleAddOpened(each, index)"
              class="footer-open"
            >
              <q-icon name="add" size="18px" class="q-mr-xs" />新增任务
            </a>
            <div
              key="add"
              v-show="each.addOpened"
              class="footer-add q-gutter-x-xs"
            >
              <q-btn
                unelevated
                dense
                size="12px"
                color="primary"
                class="footer-btn"
                label="新增"
                :loading="loading['workItem/add']"
                @click="handleAdd(each, index)"
              />
              <q-btn
                flat
                unelevated
                dense
                size="12px"
                color="primary"
                class="footer-btn"
                label="取消"
                @click="each.addOpened = false"
              />
            </div>
          </transition-group>
        </div>
      </q-list>
    </div>
    <div class="column-wrapper" v-else>
      <q-table
        :data="categories.reduce((pre, next) => pre.concat(next.workItems), [])"
        :columns="columns"
        row-key="id"
        :pagination.sync="pagination"
        flat
        class="q-pa-md full-height scroll"
      >
        <template v-slot:body-cell-assignee_users="props">
          <q-td :class="props.col.__tdClass">
            <div class="q-gutter-x-xs">
              <q-avatar
                v-for="user in props.row.assignee_users"
                :key="user.id"
                size="28px"
              >
                <q-img :src="user.avatar_url" />{{ user.name }}
              </q-avatar>
            </div>
          </q-td>
        </template>
        <template v-slot:body-cell-operation="props">
          <q-td :class="props.col.__tdClass" class="q-gutter-x-sm">
            <router-link to="" class="link">管理</router-link>
          </q-td>
        </template>
      </q-table>
    </div>

    <q-dialog seamless v-model="updateModalOpened" position="right" maximized>
      <q-layout view="lHh lpr lFf" container class="modal-content-col-9">
        <q-form @submit="handleUpdate" ref="updateForm">
          <q-header bordered class="bg-primary text-white">
            <q-toolbar>
              <q-btn flat v-close-popup round dense icon="arrow_back" />
              <q-toolbar-title>{{ updateModel.title }}</q-toolbar-title>
            </q-toolbar>
          </q-header>
          <q-page-container>
            <q-page class="column">
              <div class="col relative-position">
                <q-splitter :value="50" disable class="absolute-full">
                  <template v-slot:before>
                    <div class="q-pa-lg full-height column">
                      <div class="row">
                        <div class="col">
                          <div
                            class="text-h6 title"
                            :class="priorityClass[updateModel.priority]"
                          >
                            <span>{{ updateModel.title }}</span>
                            <q-badge
                              class="q-ml-xs"
                              v-for="label in updateModel.labels"
                              :key="label.color"
                              align="middle"
                              :style="`background: ${label.color}`"
                              >{{ label.title }}</q-badge
                            >
                          </div>
                          <div class="text-subtitle2 text-grey-9">
                            {{ updateModel.id }}
                          </div>
                          <div class="text-subtitle2 text-grey-7">
                            <router-link :to="`setting/member`" class="link">{{
                              updateModel.owner.name
                            }}</router-link>
                            <span>
                              创建于
                              {{
                                updateModel.created_at
                                  | moment('YYYY年MM月DD日')
                              }}</span
                            >
                          </div>
                        </div>
                        <div>
                          <q-avatar
                            v-for="user in updateModel.assignee_users.slice(
                              0,
                              2
                            )"
                            :key="user.id"
                            size="36px"
                          >
                            <q-img :src="user.avatar_url" />
                          </q-avatar>
                        </div>
                      </div>
                      <div>
                        <q-separator />
                      </div>
                      <div class="col scroll scrollbar-hidden q-my-md">
                        <Loading :loading="loading['workItem/fetchComment']">
                          <q-chat-message
                            v-for="comment in comments"
                            :key="comment.id"
                            :name="comment.created_by.name"
                            :avatar="comment.created_by.avatar_url"
                            :text="[comment.comment]"
                            :stamp="
                              $moment(comment.created_at).format(
                                'YYYY年MM月DD日'
                              )
                            "
                            :sent="currentUser.id === comment.created_by.id"
                          />
                        </Loading>
                      </div>
                      <q-input
                        outlined
                        v-model="$v.comment.$model"
                        type="text"
                        dense
                        @click="$v.comment.$touch"
                        placeholder="说点啥"
                        @keydown.enter="handleAddComment"
                      >
                        <template v-slot:append>
                          <q-btn
                            round
                            flat
                            color="primary"
                            :disable="$v.comment.$error"
                            icon="send"
                            size="12px"
                            @click="handleAddComment"
                          />
                        </template>
                      </q-input>
                    </div>
                  </template>
                  <template v-slot:after>
                    <div class="q-pa-lg">
                      <div class="row q-col-gutter-x-lg">
                        <div class="col-6">
                          <Field contracted>
                            <template v-slot:label>
                              <span class="field">开始日期：</span>
                            </template>
                            <q-input
                              filled
                              square
                              v-model="$v.updateModel.start_date.$model"
                              type="text"
                              bg-color="white"
                              dense
                              :rules="[
                                () =>
                                  !$v.updateModel.start_date.$error ||
                                  '请输入开始日期'
                              ]"
                              :disable="!editable"
                              mask="date"
                            >
                              <template v-slot:append v-if="editable">
                                <q-icon name="event" class="cursor-pointer">
                                  <q-popup-proxy>
                                    <q-date
                                      dense
                                      v-model="$v.updateModel.start_date.$model"
                                    />
                                  </q-popup-proxy>
                                </q-icon>
                              </template>
                            </q-input>
                          </Field>
                        </div>
                        <div class="col-6">
                          <Field contracted>
                            <template v-slot:label>
                              <span class="field">结束日期：</span>
                            </template>
                            <q-input
                              filled
                              square
                              v-model="$v.updateModel.end_date.$model"
                              type="text"
                              bg-color="white"
                              dense
                              :rules="[
                                () =>
                                  !$v.updateModel.end_date.$error ||
                                  '请输入结束日期'
                              ]"
                              :disable="!editable"
                              mask="date"
                            >
                              <template v-slot:append v-if="editable">
                                <q-icon name="event" class="cursor-pointer">
                                  <q-popup-proxy>
                                    <q-date
                                      dense
                                      v-model="$v.updateModel.end_date.$model"
                                    />
                                  </q-popup-proxy>
                                </q-icon>
                              </template>
                            </q-input>
                          </Field>
                        </div>
                      </div>
                      <Field contracted>
                        <template v-slot:label>
                          <span class="field">描述：</span>
                        </template>
                        <q-editor
                          v-model="updateModel.description"
                          dense
                          :definitions="{
                            bold: {
                              label: 'Bold',
                              icon: null,
                              tip: 'My bold tooltip'
                            }
                          }"
                          class="q-mb-md"
                          :disable="!editable"
                        />
                      </Field>
                      <Field contracted v-if="!editable">
                        <template v-slot:label>
                          <span class="field">附件：</span>
                        </template>
                        <div class="q-gutter-x-sm">
                          <a
                            v-for="attachment in updateModel.attachments"
                            :key="attachment.id"
                            class="link"
                            :href="attachment.file"
                            >{{ attachment.filename }}</a
                          >
                        </div>
                      </Field>
                      <q-uploader
                        :url="`${domain}/api/v1/attachments`"
                        :headers="[
                          { name: 'X-CSRFToken', value: getCookie('csrftoken') }
                        ]"
                        auto-upload
                        multiple
                        flat
                        bordered
                        class="uploader-container"
                        @uploaded="handleUploaded"
                        v-else
                      >
                        <template v-slot:header></template>
                        <template v-slot:list="scope">
                          <div class="uploader-content">
                            <div class="text-center q-py-lg text-grey-9">
                              拖拽文件<span class="text-weight-bold">
                                至此 </span
                              >或者<a class="uploader-link"
                                >上传文件
                                <q-uploader-add-trigger />
                              </a>
                            </div>
                            <q-list
                              separator
                              inset
                              v-if="scope.files.length > 0"
                              class="q-px-md bg-white"
                            >
                              <q-item
                                v-for="file in scope.files"
                                :key="file.name"
                              >
                                <q-item-section>
                                  <q-item-label
                                    class="text-weight-bold full-width ellipsis"
                                    >{{ file.name }}</q-item-label
                                  >
                                  <q-item-label caption>
                                    {{ file.__sizeLabel }} /
                                    {{ file.__progressLabel }}
                                  </q-item-label>
                                </q-item-section>
                                <q-item-section top side>
                                  <q-btn
                                    flat
                                    dense
                                    round
                                    icon="clear"
                                    color="grey-9"
                                    @click="scope.removeFile(file)"
                                  />
                                </q-item-section>
                              </q-item>
                            </q-list>
                          </div>
                        </template>
                      </q-uploader>
                    </div>
                  </template>
                </q-splitter>
              </div>
            </q-page>
          </q-page-container>
          <q-footer class="bg-white text-primary shadow-3">
            <q-toolbar class="q-gutter-x-sm">
              <q-space />
              <q-btn
                color="primary"
                unelevated
                label="编辑"
                @click="editable = true"
                v-show="!editable"
              />
              <template v-if="editable">
                <q-btn
                  v-if="editable"
                  color="primary"
                  unelevated
                  type="submit"
                  label="提交"
                  :loading="loading['workItem/update']"
                />
                <q-btn
                  flat
                  color="primary"
                  label="重置"
                  @click="handleResetUpload"
                />
              </template>
            </q-toolbar>
          </q-footer>
        </q-form>
      </q-layout>
    </q-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { Cookies } from 'quasar';
import { required } from 'vuelidate/lib/validators';
import Draggable from 'vuedraggable';
import Loading from '@/components/Loading';
import Field from '@/components/Field';
import TagSelect from '@/components/TagSelect';
import {
  formatOption,
  formatSelectDisplay,
  scrollToElement
} from '@/utils/utils';
import { createWorkItemModel, vars } from '../model';
import { set, get } from '@/views/setting';
const paginationKey = 'workItem/pagination';
const setPagination = set(paginationKey);
const getPagination = get(paginationKey);

export default {
  name: 'List',
  components: {
    Loading,
    Field,
    Draggable,
    TagSelect
  },
  data() {
    return {
      globalLoading: true,

      view: 'kanban',
      filter: createFilter(),

      modules: [],
      assignee_users: [],
      ...vars,
      workItemTypes: vars.workItemTypes.map(type => ({
        ...type,
        workItems: [],
        addOpened: false
      })),
      priorityClass: {
        1: 'low',
        2: 'medium',
        3: 'high'
      },

      columns: [
        {
          name: 'id',
          label: '编号',
          align: 'left',
          field: 'id',
          style: 'width: 12.5%'
        },
        {
          name: 'title',
          label: '标题',
          align: 'center',
          field: 'title',
          style: 'width: 12.5%'
        },
        {
          name: 'feature',
          label: '关联feature',
          align: 'center',
          field: row => row.feature.title,
          style: 'width: 12.5%'
        },
        {
          name: 'assignee_users',
          label: '处理人',
          align: 'center',
          field: row => row.assignee_users,
          style: 'width: 12.5%'
        },
        {
          name: 'priority',
          label: '优先级',
          align: 'center',
          field: row => formatSelectDisplay(this.priorities, row.priority),
          style: 'width: 12.5%'
        },
        {
          name: 'status',
          label: '状态',
          align: 'center',
          field: row => formatSelectDisplay(this.workItemTypes, row.status),
          style: 'width: 12.5%'
        },
        {
          name: 'end_date',
          label: '结束日期',
          align: 'center',
          field: 'end_date',
          style: 'width: 12.5%'
        },
        {
          name: 'operation',
          label: '操作',
          align: 'right',
          field: row => row,
          style: 'width: 12.5%'
        }
      ],
      pagination: getPagination(),

      addModel: createWorkItemModel(),
      updateModel: createWorkItemModel(),
      updateModelBackup: createWorkItemModel(),
      updateModalOpened: false,

      editable: false,
      domain: window.location.origin,
      comment: '',

      popupUpdateModel: createWorkItemModel()
    };
  },
  validations: {
    addModel: {
      title: { required }
    },
    updateModel: {
      start_date: { required },
      end_date: { required },
      title: { required }
    },
    popupUpdateModel: {
      title: { required }
    },
    comment: {
      required
    }
  },
  watch: {
    pagination(val) {
      setPagination({
        rowsPerPage: val.rowsPerPage
      });
    }
  },
  computed: {
    ...mapState('global', ['loading']),
    ...mapState('workItem', {
      workItems: 'list',
      comments: 'comments'
    }),
    ...mapState('user', ['currentUser']),
    ...mapState('project', {
      moduleOptions: 'modules',
      members: 'members',
      labelOptions: 'labels'
    }),
    users() {
      return this.members.map(member => member.user);
    },
    projectId() {
      return this.$route.params.projectId;
    },
    assignee_usersOptions() {
      return this.workItems.reduce(
        (pre, next) =>
          pre.concat(
            formatOption(
              next.assignee_users.filter(
                assignee_user =>
                  !pre.some(each => {
                    return each.id === assignee_user.id;
                  })
              )
            )
          ),
        []
      );
    },
    labels() {
      let labels = this.workItems.reduce(
        (pre, next) =>
          pre.concat(
            next.labels.filter(
              label =>
                !pre.some(each => {
                  return each.id === label.id;
                })
            )
          ),
        []
      );
      labels.forEach(label => {
        label.value = label.id;
      });
      return labels;
    },
    categories() {
      let categories = this.workItemTypes;
      categories.forEach(category => {
        category.workItems = [];
      });

      const { module, assignee_users, labels, isMine, progress } = this.filter;
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.workItems
        .sort((pre, next) => {
          pre.index = pre.index || 999999;
          next.index = next.index || 999999;
          if (pre.index < next.index) {
            return -1;
          }
          if (pre.index > next.index) {
            return 1;
          }
          return 0;
        })
        .forEach(workItem => {
          let isModule = true,
            includeAssignee_users = true,
            includeLabels = true,
            includeMe = true,
            gtProgress = true;
          if (module !== '') {
            isModule = workItem.module.id === module.id;
          }
          if (assignee_users.length > 0) {
            includeAssignee_users = workItem.assignee_users.some(user =>
              assignee_users.some(filter => filter.id === user.id)
            );
          }
          if (labels.length > 0) {
            includeLabels = workItem.labels.some(label =>
              labels.some(filter => {
                return filter === label.id;
              })
            );
          }
          if (isMine) {
            includeMe = workItem.owner === this.currentUser.id;
          }
          if (progress > 0) {
            gtProgress = workItem.progress > progress;
          }
          let authorized =
            isModule &&
            includeAssignee_users &&
            includeLabels &&
            includeMe &&
            gtProgress;

          if (authorized) {
            let category = categories.find(
              category => workItem.status === category.value
            );
            category.workItems.push({
              ...workItem,
              assignee_users: formatOption(workItem.assignee_users),
              labels: formatOption(workItem.labels)
            });
          }

          return authorized;
        });

      return categories;
    }
  },
  methods: {
    formatSelectDisplay,
    ...mapActions('workItem', {
      addWorkItem: 'add',
      queryWorkItem: 'fetch',
      removeWorkItem: 'remove',
      updateWorkItem: 'update',
      queryComment: 'fetchComment',
      addComment: 'addComment'
    }),
    ...mapActions('project', {
      queryModule: 'fetchModule',
      queryMember: 'fetchMember',
      queryLabel: 'fetchLabel'
    }),
    moduleFilter(val, update, abort) {
      update(() => {
        this.modules = this.moduleOptions.filter(
          module => module.name.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    assignee_usersFilter(val, update, abort) {
      update(() => {
        this.assignee_users = this.assignee_usersOptions.filter(
          assignee_user =>
            assignee_user.name.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    resetFilter() {
      this.filter = createFilter();
    },
    async handleChange({ added, removed, moved }, { value, workItems }) {
      let { element, newIndex, oldIndex } = added || removed || moved;
      if (!removed) {
        workItems.forEach((workItem, ind) => (workItem.index = ++ind));
        // for sorting
        element.index = newIndex + 0.5;
        if (moved && newIndex > oldIndex) {
          ++element.index;
        }
        element.status = value;
      } else {
        await this.updateWorkItem({
          projectId: this.projectId,
          id: element.id,
          ...element
        });
      }

      // forceUpdate
      if (moved) {
        this.filter = {
          ...this.filter
        };
      }
    },
    handleAddOpened(category, index) {
      this.categories.forEach(category => (category.addOpened = false));
      this.addModel = createWorkItemModel();
      this.$v.addModel.$reset();
      category.addOpened = true;
      // scroll to the input field
      scrollToElement(this.$refs.addForm[0].$el);
    },
    async handleAdd(category, index) {
      this.$v.addModel.$touch();
      this.$refs.addForm[index].validate();
      if (this.$v.addModel.$invalid) {
        return;
      }
      this.addModel.status = (index + 1).toString();
      await this.addWorkItem({
        projectId: this.projectId,
        ...this.addModel
      });
      category.addOpened = false;
    },
    async handleUpdateOpened(workItem) {
      this.updateModel = {
        ...workItem
      };
      this.updateModelBackup = {
        ...workItem
      };
      this.updateModalOpened = true;

      await this.queryComment({
        projectId: this.projectId,
        workItemId: workItem.id
      });
    },
    async handleUpdate() {
      this.$v.updateModel.$touch();
      this.$refs.updateForm.validate();
      if (this.$v.updateModel.$invalid) {
        return;
      }
      await this.updateWorkItem({
        projectId: this.projectId,
        ...this.updateModel
      });
      this.updateModelBackup = {
        ...this.updateModel
      };

      this.editable = false;
    },
    getCookie(key) {
      return Cookies.get(key);
    },
    handleUploaded({ files, xhr }) {
      const resp = JSON.parse(xhr.responseText);
      this.updateModel.attachments.push(resp.data);
    },
    handleResetUpload() {
      this.editable = false;
      this.updateModel = {
        ...(this.updateModelBackup || createWorkItemModel())
      };
    },
    handleUpdatePopupWorkItemOpened(workItem) {
      this.popupUpdateModel = {
        ...workItem
      };
      this.$v.popupUpdateModel.$reset();
    },
    async handleUpdatePopupWorkItem(workItem = this.popupUpdateModel) {
      this.$v.popupUpdateModel.$touch();
      this.$refs.workItemPopupForm[0].validate();
      if (this.$v.popupUpdateModel.$invalid) {
        return;
      }
      this.$refs['workItem-popup-title'][0].blur();
      await this.updateWorkItem({
        projectId: this.projectId,
        ...workItem
      });
    },
    async handleAddComment({ id }) {
      if (this.$v.comment.$invalid) {
        return;
      }
      await this.addComment({
        projectId: this.projectId,
        workItemId: this.updateModel.id,
        comment: this.comment
      });
      this.comment = '';
    }
  },
  async created() {
    let project = {
      projectId: this.projectId
    };
    await this.queryWorkItem(project);
    await this.queryModule(project);
    await this.queryMember(project);
    await this.queryLabel(project);

    this.globalLoading = false;
  },
  mounted() {}
};

function createFilter() {
  return {
    module: '',
    assignee_users: [],
    labels: [],
    isMine: false,
    progress: 0
  };
}
</script>

<style lang="stylus" scoped>
$column-bg = white;
$item-bg = $grey-3;

.board
  user-select: none;
  overflow: hidden;
  height: calc(100vh - 50px);
  position: relative;
  .column-wrapper
    padding: 16px;
    white-space: nowrap;
    overflow-x: auto;
    overflow-y: hidden;
    position: absolute;
    top: 50px;
    right: 0;
    bottom: 0;
    left: 0;
  .board-column
    display: inline-block;
    height: 100%;
    width: 25%;
    max-width: 341.75px;
    overflow: hidden;
  .container
    max-height: 100%;
    padding: 8px;
    overflow: hidden;
    border-radius: $generic-border-radius;
    background: $column-bg;
    position: relative;
    display: flex;
    flex-direction: column;
  .header
    position: absolute;
    z-index: 10;
    top: 0;
    left: 0;
    right: 0;
    padding: 0 8px;
    height: 38px;
    background: $column-bg;
    color: $blue-grey-9;
    font-size: 14px;
    font-weight: $text-weights.bold;
  .body
    margin: 30px 0;
  .footer
    position: absolute;
    z-index: 10;
    bottom: 0;
    left: 0;
    right: 0;
    height: 38px;
    color: $blue-grey-9;
    font-weight: $text-weights.medium;
    overflow: hidden;
    .footer-open
      width: 100%;
      height: 38px;
      display: flex;
      align-items: center;
      padding: 0 8px;
      background: $column-bg;
      &:hover
        background: $grey-4;
        color: $blue-grey-9;
    .footer-add
      width: 100%;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding: 0 8px;
      background: $column-bg;
      .footer-btn
        padding: 0 8px;

.item
  position: relative;
  display: block;
  padding: 6px 8px;
  background: $item-bg;
  color: $blue-grey-9;
  border-radius: $generic-border-radius;
  overflow: hidden;
  &.sortable-ghost
    background: $grey-4 !important;
    >*
      opacity: 0;
  &:before
    display: block;
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 2px;
    .low&
      background: $positive;
    .medium&
      background: $warning;
    .high&
      background: $red;

.toolbar-control
  height: 36px;
  font-weight: $text-weights.medium;
.toolbar-search
  min-width: 200px;
  max-width: 200px;
  max-height: 40px;
  border-radius: $generic-border-radius;
.option
  color: $grey-9;
  &.selected
    color: $primary;
.popup-setting
  width: 500px;
  min-height: 200px;
  background: white;
  position: relative;
.btn-setting
  width: 40px;
.btn-reset
  position: absolute;
  right: 16px;
  bottom: 8px;
  color: $primary;
  &:hover
    text-decoration: underline;
    color: $teal-4;

.gutter-avatar
  >div
    margin-left: -14px;
    position: relative;
    transition: .3s;
  &:hover
    >div
      margin-left: 0;

.title
  padding-left: 6px;
  position: relative;
  &:before
    display: block;
    content: '';
    position: absolute;
    top: 6px;
    left: 0;
    bottom: 6px;
    width: 2px;
    .low&
      background: $positive;
    .medium&
      background: $warning;
    .high&
      background: $red;

.field
  font-weight: $text-weights.medium;
  color: $blue-grey-6;
.workItem-popup
  width: 300px;
  background: white;
  position: relative;
</style>
