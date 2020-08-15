document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.likelink').forEach(link => {
        link.onclick = function() {
            // console.log(this.dataset.postid)
            // fetch(`/likepost/`)
            const postid = this.dataset.postid
            const curr = document.querySelector(`#span${postid}`);
            fetch(`/togglelike/${postid}`);

            if (this.innerHTML === 'like') {
                this.innerHTML = 'unlike';
                curr.innerHTML = parseInt(curr.innerHTML) + 1;
            } else {
                this.innerHTML = 'like';
                curr.innerHTML = parseInt(curr.innerHTML) - 1;
            }
        };
    });

    document.querySelectorAll('.editpost').forEach(link => {
        link.onclick = function() {
            if (this.innerHTML === 'Edit') {
                this.innerHTML = 'save changes';
                let p = this.parentElement.childNodes[3];
                let ta = document.createElement('textarea');
                ta.innerHTML = p.innerHTML;
                ta.className = 'form-control';
                p.parentNode.replaceChild(ta, p);
            } else {
                var formData = new FormData();
                formData.append('content', this.parentElement.childNodes[3].value);
                formData.append('postid', this.id.slice(4));

                fetch(`/editpost`, {
                    method: 'POST',
                    body: formData,
                })

                this.innerHTML = 'Edit';
                let ta = this.parentElement.childNodes[3];
                let p = document.createElement('p');
                p.innerHTML = ta.value;
                p.className = 'card-text';
                ta.parentNode.replaceChild(p, ta);

            }
        };
    });

    document.querySelector('#fb').onclick = () => {
        const button = document.querySelector('#fb');
        const curr = document.querySelector('#followno');
        const userdisid = button.dataset.id;

        fetch(`/togglefollow/${userdisid}`);

        if (button.innerHTML.trim() === 'Follow') {
            button.innerHTML = 'Unfollow';
            curr.innerHTML = parseInt(curr.innerHTML) + 1;

        } else {
            button.innerHTML = 'Follow';
            curr.innerHTML = parseInt(curr.innerHTML) - 1;
        }
    };

});