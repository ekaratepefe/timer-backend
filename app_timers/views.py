from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Label
from .models import TimerSession, TimerBlock
from django.shortcuts import get_object_or_404

from .models import Label, TimerBlock, TimerSession, CustomUser
from .serializers import (
    LabelSerializer,
    LabelCreateSerializer,
    LabelDetailSerializer,
    LabelNoteSerializer,
    WorkBlockListSerializer,
    FilteredWorkBlockSerializer,
    CreateTimerBlockSerializer,
    TimerBlockDetailSerializer,
    TimerBlockNoteSerializer,
    AddToSessionSerializer,
    RemoveFromSessionSerializer,
    WorkBlockStatsSerializer,
    StartWorkBlockSerializer,
    PauseWorkBlockSerializer,
    ContinueWorkBlockSerializer,
    StopWorkBlockSerializer,
)


# API to list all labels of a user
class LabelListAPIView(generics.ListAPIView):
    """
    ## 📄 **Label List API**

    🔗 **API URL:** `api/labels/`

    API that retrieves a list of all labels belonging to the authenticated user.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

        - Example Request:
        ```shell
        curl -X GET http://example.com/labels/ \
        -H "Authorization: Bearer <token>"
        ```

    - 📤 **Output:**
        - ✅ **Successful Label Retrieval:**
            - If request is successful:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                [
                    {
                        "id": 1,
                        "title": "Work",
                        "description": "Work-related tasks"
                    },
                    {
                        "id": 2,
                        "title": "Study",
                        "description": "Study-related topics"
                    }
                ]
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)


class LabelCreateAPIView(generics.CreateAPIView):
    """
    ## 📄 **Label Creation API**

    🔗 **API URL:** `api/labels/create/`

    API that creates a new label for the authenticated user.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Request Body (JSON):**
            - **title (string):** Title of the new label.
            - **description (string, optional):** Description of the new label.

        - 📄 Example JSON Input:
        ```json
        {
            "title": "Study",
            "description": "Study-related topics"
        }
        ```

    - 📤 **Output:**
        - ✅ **Successful Label Creation:**
            - If label is created successfully:
                - ✅ Status: 201 Created
                - 📄 Response JSON:
                ```json
                {
                    "id": 2,
                    "title": "Study",
                    "description": "Study-related topics"
                }
                ```

        - ❌ **Conflict:**
            - If a label with the same title already exists for the user:
                - ❌ Status: 409 Conflict
                - 📄 Response JSON: `{"detail": "A label with this title already exists."}`

        - ❌ **Invalid Input:**
            - If the input data is invalid:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"title": ["This field is required."]}`
    """
    serializer_class = LabelCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user to the label before saving
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")

        # Check if a label with the same title already exists for the user
        if Label.objects.filter(user=request.user, title=title).exists():
            return Response({"detail": "A label with this title already exists."}, status=status.HTTP_409_CONFLICT)

        return super().create(request, *args, **kwargs)


class LabelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    ## 📄 **Detail - Update - Delete Label (with ID)**

    🔗 **API URL:** `api/labels/<int:pk>/`

    API that retrieves, updates, or deletes a specific label (excluding the notes field).

    - 📨 **HTTP Method(s):** GET, PUT, DELETE

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Request Body (JSON - for PUT only):**
            - **title (string):** Updated title of the label.
            - **description (string, optional):** Updated description of the label.

        - 📄 Example JSON Input for Update:
        ```json
        {
            "title": "Updated Title",
            "description": "Updated description"
        }
        ```

    - 📤 **Output:**
        - ✅ **Successful Label Retrieval:**
            - If label is retrieved successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "id": 1,
                    "title": "Work",
                    "description": "Work-related tasks"
                }
                ```

        - ✅ **Successful Label Update:**
            - If label is updated successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "id": 1,
                    "title": "Updated Title",
                    "description": "Updated description"
                }
                ```

        - ✅ **Successful Label Deletion:**
            - If label is deleted successfully:
                - ✅ Status: 204 No Content

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    serializer_class = LabelDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)


class LabelDetailOfTitleView(APIView):
    """
    ## 📄 **Find Label (With Title)**

    🔗 **API URL:** `api/labels/retrieve/`

    API to retrieve a label by its title for the authenticated user.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Parameters:**
            - **title (string):** Title of the label to be retrieved.

        - Example Request:
        {
        "title": "My Label"
        }

    - 📤 **Output:**
        - ✅ **Successful Retrieval:**
            - If the label is found:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "id": 1,
                    "title": "My Label",
                    "description": "This is a label description.",
                    "notes": "Some notes about the label."
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the label does not exist for the authenticated user:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Label not found."}`
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        user = request.user

        # Kullanıcı ve title ile Label'ı bul
        label = get_object_or_404(Label, user=user, title=title)

        # Label detaylarını döndür
        return Response({
            "id": label.id,
            "title": label.title,
            "description": label.description,
        }, status=status.HTTP_200_OK)


class LabelNoteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    ## 📄 **Detail - Update - Delete Label Notes**

    🔗 **API URL:** `api/labels/<int:pk>/notes/`

    API that retrieves, updates, or deletes the note of a specific label. Deleting a note will set it to an empty string.

    - 📨 **HTTP Method(s):**
        - **GET:** Retrieve the note.
        - **PUT:** Update the note content.
        - **DELETE:** Clear the note (set it to an empty string).

    - 📥 **Input (for PUT):**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Request Body (JSON):**
            - **notes (string):** Updated content of the note. Set to an empty string to delete the note.

        - 📄 Example JSON Input for PUT:
        ```json
        {
            "notes": "Updated note content"
        }
        ```

    - 📤 **Output (for PUT):**
        - ✅ **Successful Note Update:**
            - If the note is updated successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "notes": "Updated note content"
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

    - 📥 **Input (for DELETE):**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

    - 📤 **Output (for DELETE):**
        - ✅ **Successful Note Clear:**
            - If the notes are cleared successfully:
                - ✅ Status: 204 No Content
                - 📄 Response JSON: `{"message": "Notes cleared successfully."}`

    - 📤 **Output (for GET):**
            - ✅ Status: 200 OK
            - 📄 Response JSON:
                ```json
                {
                    "notes": "note content"
                }
                ```
    """
    serializer_class = LabelNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Save the note, can be empty to delete it
        serializer.save(notes=self.request.data.get('notes', ""))

    def perform_destroy(self, instance):
        # Instead of deleting the Label, clear the 'notes' field
        instance.notes = ""
        instance.save()


class WorkBlockListAPIView(generics.ListAPIView):
    """
    ## 📄 **Work Block List API**

    🔗 **API URL:** `api/work-blocks/`

    API that retrieves a list of all work blocks of the authenticated user, ordered from the most recent to the oldest.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

        - Example Request:
        ```shell
        curl -X GET http://example.com/work-blocks/ \
        -H "Authorization: Bearer <token>"
        ```

    - 📤 **Output:**
        - ✅ **Successful Work Block Retrieval:**
            - If request is successful:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                [
                    {
                        "id": 1,
                        "label": "Study",
                        "work_duration": 50,
                        "break_duration": 10,
                        "percentage_of_completion": 80
                    },
                    {
                        "id": 2,
                        "label": "Work",
                        "work_duration": 60,
                        "break_duration": 15,
                        "percentage_of_completion": 100
                    }
                ]
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    serializer_class = WorkBlockListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user).order_by('-created_at')


# API to retrieve filtered work blocks with no repetition
class FilteredWorkBlockAPIView(generics.ListAPIView):
    """
    ## 📄 **Filtered Work Block List API**

    🔗 **API URL:** `api/work-blocks/filtered/`

    API that retrieves a list of work blocks filtered by label, work duration, and break duration, with no repetitions.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Query Parameters:**
            - **n (integer):** Number of recent work blocks to retrieve.

        - Example Request:
        ```shell
        curl -X GET http://example.com/work-blocks/filtered/?n=5 \
        -H "Authorization: Bearer <token>"
        ```

    - 📤 **Output:**
        - ✅ **Successful Filtered Work Block Retrieval:**
            - If request is successful:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                [
                    {
                        "label": "Study",
                        "work_duration": 50,
                        "break_duration": 10
                    },
                    {
                        "label": "Work",
                        "work_duration": 60,
                        "break_duration": 15
                    }
                ]
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    serializer_class = FilteredWorkBlockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Custom queryset to remove repetition
        user_blocks = TimerBlock.objects.filter(user=self.request.user).order_by('-created_at')
        unique_blocks = {}
        for block in user_blocks:
            key = (block.label.title, block.work_duration, block.break_duration)
            if key not in unique_blocks:
                unique_blocks[key] = block
        return list(unique_blocks.values())[:self.request.query_params.get('n', 10)]


class CreateTimerBlockView(generics.CreateAPIView):
    """
    ## 📄 **Create Work Block API**

    🔗 **API URL:** `api/timer-blocks/`

    API to create a new work block for the authenticated user.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **label (string):** The label for the work block.
            - **work_duration (integer):** Duration for the work session in minutes.
            - **break_duration (integer):** Duration for the break in minutes.
            - **note_title (string):** Title for the notes associated with the work block.
            - **note_description (string):** Description for the notes associated with the work block.

        - Example Request:
        ```shell
        curl -X POST http://example.com/api/timer-blocks/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"label": "Study", "work_duration": 50, "break_duration": 10, "note_title": "Math Notes", "note_description": "Review chapter 1."}'
        ```

        {
    "label": null,
    "work_duration": null,
    "break_duration": null,
    "note_title": "",
    "note_description": ""
}

    - 📤 **Output:**
        - ✅ **Successful Work Block Creation:**
            - If the work block is created successfully:
                - ✅ Status: 201 Created
                - 📄 Response JSON:
                ```json
                {
                    "id": 1,
                    "label": "Study",
                    "work_duration": 50,
                    "break_duration": 10,
                    "note_title": "Math Notes",
                    "note_description": "Review chapter 1."
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    serializer_class = CreateTimerBlockSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TimerBlockDetailView(generics.RetrieveAPIView):
    """
    ## 📄 **Work Block Detail API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/`

    API to retrieve the details of a specific work block for the authenticated user.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

    - 📤 **Output:**
        - ✅ **Successful Work Block Retrieval:**
            - If the request is successful:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "id": 1,
                    "label": "Study",
                    "work_duration": 50,
                    "break_duration": 10,
                    "note_title": "Math Notes",
                    "note_description": "Review chapter 1."
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = TimerBlockDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)


class TimerBlockNoteView(generics.RetrieveUpdateDestroyAPIView):
    """
    ## 📄 **Work Block Note API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/notes/`

    API to retrieve, update, or delete notes associated with a specific work block.

    - 📨 **HTTP Method:** GET, PATCH, DELETE

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        {
         "note": "",
         "note_title": "",
         "note_description": ""
        }

    - 📤 **Output:**
        - ✅ **Successful Note Retrieval:**
            - If the note is retrieved successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "note_title": "Math Notes",
                    "note_description": "Review chapter 1."
                }
                ```

        - ✅ **Successful Note Update:**
            - If the note is updated successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "note_title": "Updated Title",
                    "note_description": "Updated Description."
                }
                ```

        - ✅ **Successful Note Deletion:**
            - If the note is deleted successfully (note cleared):
                - ✅ Status: 204 No Content

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = TimerBlockNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.note = ""
        instance.note_title = ""
        instance.note_description = ""
        instance.save()


class AddToSessionView(generics.GenericAPIView):
    """
    ## 📄 **Add Work Block to Session API**

    🔗 **API URL:** `api/session/add-work-block/`

    API to add a specific work block to the user's session.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **timer_block_id (integer):** ID of the work block to be added.

        - Example Request:
        ```shell
        curl -X POST http://example.com/api/session/add-work-block/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"timer_block_id": 1}'
        ```

    - 📤 **Output:**
        - ✅ **Successful Addition to Session:**
            - If the work block is added successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "message": "Timer Block added to session."
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = AddToSessionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            timer_block_id = request.data.get("timer_block_id")
            TimerBlock.objects.get(id=timer_block_id)
            session = TimerSession.objects.get(user=request.user)
        except TimerBlock.DoesNotExist:
            return Response({"detail": "Timer Block not found."}, status=status.HTTP_404_NOT_FOUND)
        except TimerSession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the timer block ID if it's not already in the session
        if timer_block_id not in session.timer_blocks.split('\n'):
            session.timer_blocks += f"{timer_block_id}\n"
            session.save()
            return Response({"message": "Timer Block added to session."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Timer Block already in session."}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromSessionView(generics.DestroyAPIView):
    """
    ## 📄 **Remove Work Block from Session API**

    🔗 **API URL:** `api/session/remove-work-block/`

    API to remove a specific work block from the user's session.

    - 📨 **HTTP Method:** DELETE

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **timer_block_id (integer):** ID of the work block to be removed.

        - Example Request:
        ```shell
        curl -X DELETE http://example.com/api/session/remove-work-block/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"timer_block_id": 1}'
        ```

        {
        "timer_block_id": 1
        }

    - 📤 **Output:**
        - ✅ **Successful Removal from Session:**
            - If the work block is removed successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "message": "Timer Block removed from session."
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`

        - ❌ **Validation Error:**
            - If the timer_block_id is not part of the session's timer_blocks:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"detail": "Timer Block ID not found in session."}`
    """
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            timer_block_id = request.data.get("timer_block_id")
            TimerBlock.objects.get(id=timer_block_id)
            session = TimerSession.objects.get(user=request.user)
        except TimerBlock.DoesNotExist:
            return Response({"detail": "Timer Block not found."}, status=status.HTTP_404_NOT_FOUND)
        except TimerSession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        # Timer block ID'yi kontrol et ve sil
        timer_blocks_list = session.timer_blocks.split('\n')
        if str(timer_block_id) in timer_blocks_list:
            timer_blocks_list.remove(str(timer_block_id))
            session.timer_blocks = '\n'.join(timer_blocks_list)
            session.save()
            return Response({"message": "Timer Block removed from session."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Timer Block ID not found in session."}, status=status.HTTP_400_BAD_REQUEST)

class WorkBlockStatsView(generics.UpdateAPIView):
    """
    ## 📄 **Work Block Statistics Update API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/stats/`

    API to update the statistics of a specific work block.

    - 📨 **HTTP Method:** PATCH

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **used_duration (integer):** The duration of time used for the work block.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/timer-blocks/1/stats/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"used_duration": 30}'
        ```

    {
    "used_duration": 6
    }

    - 📤 **Output:**
        - ✅ **Successful Statistics Update:**
            - If the statistics are updated successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "percentage_of_completion": 60.0
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = WorkBlockStatsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            timer_block_id = kwargs['pk']
            used_duration = request.data.get("used_duration")

            timer_block = TimerBlock.objects.get(id=timer_block_id, user=request.user)
            # Call to the statistics calculation function should be here
            timer_block.used_duration = int(used_duration)
            timer_block.percentage_of_completion = int(self.calculate_percentage(timer_block))
            timer_block.save()

            return Response({
                "percentage_of_completion": timer_block.percentage_of_completion
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def calculate_percentage(self, timer_block):
        # You can fill in the percentage calculation function here
        return (timer_block.used_duration / timer_block.work_duration) * 100 if timer_block.work_duration > 0 else 0


class StartWorkBlockView(generics.UpdateAPIView):
    """
    ## 📄 **Start Work Block API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/start/`

    API to start a specific work block.

    - 📨 **HTTP Method:** PATCH

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **used_duration (integer):** The duration of time used for the work block.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/timer-blocks/1/start/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"used_duration": 20}'
        ```
        {
    "used_duration": 5
}

    - 📤 **Output:**
        - ✅ **Successful Work Block Start:**
            - If the work block is started successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "percentage_of_completion": 20.0
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = StartWorkBlockSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            timer_block_id = kwargs['pk']
            used_duration = request.data.get("used_duration")

            timer_block = TimerBlock.objects.get(id=timer_block_id, user=request.user)
            timer_block.is_started = True
            timer_block.used_duration = used_duration
            timer_block.started_at = timezone.now()
            timer_block.percentage_of_completion = self.calculate_percentage(timer_block)
            timer_block.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            "percentage_of_completion": timer_block.percentage_of_completion
        }, status=status.HTTP_200_OK)

    def calculate_percentage(self, timer_block):
        # You can fill in the percentage calculation function here
        return (timer_block.used_duration / timer_block.work_duration) * 100 if timer_block.work_duration > 0 else 0


class PauseWorkBlockView(generics.UpdateAPIView):
    """
    ## 📄 **Pause Work Block API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/pause/`

    API to pause a specific work block.

    - 📨 **HTTP Method:** PATCH

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **used_duration (integer):** The duration of time used for the work block.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/timer-blocks/1/pause/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"used_duration": 10}'
        ```
    {
    "used_duration": 5
    }

    - 📤 **Output:**
        - ✅ **Successful Work Block Pause:**
            - If the work block is paused successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "percentage_of_completion": 50.0
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = PauseWorkBlockSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            timer_block_id = kwargs['pk']
            used_duration = request.data.get("used_duration")

            timer_block = TimerBlock.objects.get(id=timer_block_id, user=request.user)
            if not timer_block.number_of_stop:
                timer_block.number_of_stop = 0
            timer_block.number_of_stop = str(int(timer_block.number_of_stop) + 1)
            timer_block.used_duration = used_duration
            timer_block.percentage_of_completion = self.calculate_percentage(timer_block)
            timer_block.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            "percentage_of_completion": timer_block.percentage_of_completion
        }, status=status.HTTP_200_OK)

    def calculate_percentage(self, timer_block):
        # You can fill in the percentage calculation function here
        return (timer_block.used_duration / timer_block.work_duration) * 100 if timer_block.work_duration > 0 else 0


class ContinueWorkBlockView(generics.UpdateAPIView):
    """
    ## 📄 **Continue Work Block API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/continue/`

    API to continue a specific work block.

    - 📨 **HTTP Method:** PATCH

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **used_duration (integer):** The duration of time used for the work block.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/timer-blocks/1/continue/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"used_duration": 25}'
        ```
        {
        "used_duration": 5
        }

    - 📤 **Output:**
        - ✅ **Successful Work Block Continue:**
            - If the work block is continued successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "percentage_of_completion": 80.0
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = ContinueWorkBlockSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            timer_block_id = kwargs['pk']
            used_duration = request.data.get("used_duration")

            timer_block = TimerBlock.objects.get(id=timer_block_id, user=request.user)
            if not timer_block.number_of_continue:
                timer_block.number_of_continue = 0
            timer_block.number_of_continue = str(int(timer_block.number_of_continue) + 1)
            timer_block.used_duration = used_duration
            timer_block.percentage_of_completion = self.calculate_percentage(timer_block)
            timer_block.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            "percentage_of_completion": timer_block.percentage_of_completion
        }, status=status.HTTP_200_OK)

    def calculate_percentage(self, timer_block):
        # You can fill in the percentage calculation function here
        return (timer_block.used_duration / timer_block.work_duration) * 100 if timer_block.work_duration > 0 else 0


class StopWorkBlockView(generics.UpdateAPIView):
    """
    ## 📄 **Stop Work Block API**

    🔗 **API URL:** `api/timer-blocks/<int:pk>/stop/`

    API to stop a specific work block.

    - 📨 **HTTP Method:** PATCH

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.
        - 📝 **Body:**
            - **used_duration (integer):** The duration of time used for the work block.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/timer-blocks/1/stop/ \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"used_duration": 40}'
        ```
        {
        "used_duration": 5
        }

    - 📤 **Output:**
        - ✅ **Successful Work Block Stop:**
            - If the work block is stopped successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                {
                    "percentage_of_completion": 100.0
                }
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the work block does not exist:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Not found."}`
    """
    serializer_class = StopWorkBlockSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            timer_block_id = kwargs['pk']
            used_duration = request.data.get("used_duration")

            timer_block = TimerBlock.objects.get(id=timer_block_id, user=request.user)
            timer_block.is_completed = True
            timer_block.used_duration = used_duration
            timer_block.percentage_of_completion = self.calculate_percentage(timer_block)
            timer_block.completed_at = timezone.now()
            timer_block.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "percentage_of_completion": timer_block.percentage_of_completion
        }, status=status.HTTP_200_OK)

    def calculate_percentage(self, timer_block):
        # You can fill in the percentage calculation function here
        return (timer_block.used_duration / timer_block.work_duration) * 100 if timer_block.work_duration > 0 else 0


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TimerSession, TimerBlock
from .serializers import TimerBlockSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404


class ListWorkBlocksInSessionView(APIView):
    """
    ## 📄 **List Work Blocks in Session API**

    🔗 **API URL:** `api/session/work-blocks/`

    This API retrieves all work blocks in the user's current session based on the order of IDs stored in the `timer_blocks` field of the `TimerSession` model.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

        - Example Request:
        ```shell
        curl -X GET http://example.com/api/session/work-blocks/ \
        -H "Authorization: Bearer <token>"
        ```

    - 📤 **Output:**
        - ✅ **Successful Retrieval:**
            - If the request is successful:
                - ✅ Status: 200 OK
                - 📄 Response JSON:
                ```json
                [
                    {
                        "id": 1,
                        "label": "Study",
                        "note_title": "math",
                        "work_duration": "50",
                        "break_duration": "10"
                        "percentage_of_completion": "0"
                    },
                    {
                        "id": 2,
                        "label": "Work",
                        "note_title": "math",
                        "work_duration": 60,
                        "break_duration": 15
                        "percentage_of_completion": "0"
                    }
                ]
                ```

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

        - ❌ **Not Found:**
            - If the session does not exist for the user:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"detail": "Session not found."}`
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        session, created = TimerSession.objects.get_or_create(user=user)  # Ensure session exists

        # Handle the case where timer_blocks might be None
        block_ids = session.timer_blocks.strip().split("\n") if session.timer_blocks else []
        valid_blocks = []
        for block_id in block_ids:
            try:
                # Check if the TimerBlock with the given ID exists
                timer_block = TimerBlock.objects.get(id=int(block_id))
                valid_blocks.append({
                    "id": str(timer_block.id),
                    "label": str(timer_block.label),
                    "note_title": str(timer_block.note_title),
                    "work_duration": str(timer_block.work_duration),
                    "break_duration": str(timer_block.break_duration),
                    "percentage_of_completion": str(timer_block.percentage_of_completion)
                })
            except TimerBlock.DoesNotExist:
                continue  # Ignore invalid block IDs

        return Response(data=valid_blocks, status=status.HTTP_200_OK)


class ResetSessionView(APIView):
    """
    ## 📄 **Reset User Session API**

    🔗 **API URL:** `api/session/reset/`

    API to reset the user's session, clearing the timer_blocks field.

    - 📨 **HTTP Method:** GET

    - 📥 **Input:**
        - 🛂 **Authorization Header (string):** Bearer token for the authenticated user.

        - Example Request:
        ```shell
        curl -X PATCH http://example.com/api/session/reset/ \
        -H "Authorization: Bearer <token>"
        ```

    - 📤 **Output:**
        - ✅ **Successful Session Reset:**
            - If the session is reset successfully:
                - ✅ Status: 200 OK
                - 📄 Response JSON: `{"detail": "Session reset successfully."}`

        - ❌ **Unauthorized Access:**
            - If the user is not authenticated:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        session = get_object_or_404(TimerSession, user=user)
        session.timer_blocks = ""
        session.save()

        return Response({"detail": "Session reset successfully."}, status=status.HTTP_200_OK)
